from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from app.services.scraper import fetch_team_standings
from app.services.grouped_league_scraper import fetch_multi_group_standings
from app.schemas.tff_models import StandingsResponse
from app.core.config import settings

router = APIRouter()


@router.get("/standings/{league_name}", response_model=StandingsResponse)
@cache(expire=settings.CACHE_EXPIRE)
async def get_simple_standings(league_name: str):
    page_id = settings.LEAGUES.get(league_name.lower())

    if not page_id:
        if league_name.lower() in settings.MULTI_GROUP_LEAGUES:
            raise HTTPException(
                status_code=400,
                detail=f"League '{league_name}' has multiple groups. Please use /api/multi-standings/{league_name}/{{group_index}}"
            )
        raise HTTPException(status_code=404, detail="League not found.")

    try:
        return await fetch_team_standings(page_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/multi-standings/{league_name}/{group_index}", response_model=StandingsResponse)
@cache(expire=settings.CACHE_EXPIRE)
async def get_multi_group_standings(league_name: str, group_index: int):
    page_id = settings.MULTI_GROUP_LEAGUES.get(league_name.lower())

    if not page_id:
        raise HTTPException(
            status_code=404,
            detail=f"Multi-group league '{league_name}' not found. Supported: {list(settings.MULTI_GROUP_LEAGUES.keys())}"
        )

    try:
        return await fetch_multi_group_standings(page_id, group_index=group_index)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
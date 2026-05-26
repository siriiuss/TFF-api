from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from app.services.scraper import fetch_team_standings
from app.services.grouped_league_scraper import fetch_multi_group_standings
from app.services.penalty_scraper import fetch_penalty_records
from app.schemas.tff_models import StandingsResponse, PenaltyResponse
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


@router.get("/penalties/{league_name}/{season}", response_model=PenaltyResponse)
@cache(expire=settings.CACHE_EXPIRE)
async def get_penalty_records(league_name: str, season: str):
    display_name = settings.PENALTY_LEAGUES.get(league_name.lower())

    if not display_name:
        raise HTTPException(
            status_code=404,
            detail=f"League '{league_name}' not found. Supported: {list(settings.PENALTY_LEAGUES.keys())}"
        )

    season_parts = season.split("-")
    if len(season_parts) != 2 or not all(p.isdigit() and len(p) == 4 for p in season_parts):
        raise HTTPException(
            status_code=400,
            detail="Season must be in 'YYYY-YYYY' format, e.g. '2025-2026'."
        )

    try:
        return await fetch_penalty_records(display_name, season)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

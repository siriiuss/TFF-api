import httpx
from bs4 import BeautifulSoup
from app.schemas.tff_models import TeamStanding, StandingsResponse
from app.core.config import settings
from datetime import datetime


async def fetch_team_standings(page_id: str) -> StandingsResponse:
    url = f"{settings.TFF_URL}{page_id}"

    async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise Exception(f"Error raised while connecting to TFF website: {e}")

    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find("table", {"class": "s-table"})
    if not table:
        raise Exception(f"Failed to fint score table named: {table}")

    rows = table.find_all("tr")[1:]
    standings_list = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 9: continue

        raw_info = cols[0].text.strip()
        rank, team_name = raw_info.split(".", 1) if "." in raw_info else (0, raw_info)

        team_data = TeamStanding(
            rank=int(rank),
            team_name=team_name.strip(),
            played=int(cols[1].text.strip()),
            won=int(cols[2].text.strip()),
            drawn=int(cols[3].text.strip()),
            lost=int(cols[4].text.strip()),
            goals_for=int(cols[5].text.strip()),
            goals_against=int(cols[6].text.strip()),
            goal_difference=int(cols[7].text.strip()),
            points=int(cols[8].text.strip())
        )
        standings_list.append(team_data)

    return StandingsResponse(
        league_name=f"League ID: {page_id}",
        season="2025-2026",
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data=standings_list
    )
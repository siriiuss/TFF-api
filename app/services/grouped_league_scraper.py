import httpx
import re
from bs4 import BeautifulSoup
from app.schemas.tff_models import TeamStanding, StandingsResponse
from app.core.config import settings
from datetime import datetime

async def fetch_multi_group_standings(page_id: str, group_index: int = 0) -> StandingsResponse:
    base_url = f"{settings.TFF_URL}{page_id}"

    async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
        response = await client.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        group_links = soup.find_all("a", href=re.compile(r"grupID=(\d+)", re.IGNORECASE))

        unique_groups = []
        seen_ids = set()

        for link in group_links:
            match = re.search(r"grupID=(\d+)", link["href"], re.IGNORECASE)
            if match:
                g_id = match.group(1)
                if g_id not in seen_ids:
                    seen_ids.add(g_id)
                    unique_groups.append({
                        "id": g_id,
                        "name": link.text.strip()
                    })

        if not unique_groups:
            return parse_html_to_standings(soup, page_id, group_name="Genel/1. Grup")

            # Validate the requested index
        if group_index < 0 or group_index >= len(unique_groups):
            raise Exception(
                f"Invalid group index. This league has {len(unique_groups)} groups available."
            )

        target_group = unique_groups[group_index]
        grup_id = target_group["id"]
        group_name = target_group["name"]

        group_url = f"{base_url}&grupID={grup_id}"
        group_response = await client.get(group_url)
        group_response.raise_for_status()
        group_soup = BeautifulSoup(group_response.content, "lxml")

        return parse_html_to_standings(group_soup, page_id, group_name=group_name)

def parse_html_to_standings(soup: BeautifulSoup, page_id: str, group_name: str) -> StandingsResponse:
    table = soup.find("table", {"class": "s-table"})
    if not table:
        raise Exception(
            f"Puan tablosu bulunamadı! TFF '{group_name}' için tabloyu henüz oluşturmamış veya tablo class'ı değişmiş olabilir."
        )

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
        league_name=f"League ID: {page_id} - {group_name}",
        season="2025-2026",
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data=standings_list
    )
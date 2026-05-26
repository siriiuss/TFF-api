import re
import json
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from app.core.config import settings
from app.schemas.tff_models import PenaltyRecord, PenaltyResponse

_PREFIX = "ctl00$MPane$m_633_3254_ctnr$m_633_3254$"
_SEL = _PREFIX + "SezonLigMacOrgKulupSelector1$"


def _season_value(season: str) -> str:
    """'2025-2026' -> '25'  (first year minus 2000)"""
    return str(int(season.split("-")[0]) - 2000)


def _extract_asp_state(html_bytes: bytes) -> dict:
    html = html_bytes.decode("windows-1254", errors="replace")

    def _find(name: str) -> str:
        m = re.search(rf'<input[^>]*name="{re.escape(name)}"[^>]*value="([^"]*)"', html)
        return m.group(1) if m else ""

    return {
        "__VIEWSTATE": _find("__VIEWSTATE"),
        "__VIEWSTATEGENERATOR": _find("__VIEWSTATEGENERATOR"),
        "__EVENTVALIDATION": _find("__EVENTVALIDATION"),
    }


def _extract_season_index(html_bytes: bytes, sv: str) -> str:
    """Parse the cmbSezon Telerik script to find the index for the requested season value."""
    html = html_bytes.decode("windows-1254", errors="replace")
    soup = BeautifulSoup(html, "lxml")
    for script in soup.find_all("script"):
        text = script.string or ""
        if "SezonLigMacOrgKulupSelector1_cmbSezon" in text and "Initialize" in text:
            m = re.search(r",\s*(\[\{.*?\}\])\s*\)", text, re.DOTALL)
            if m:
                try:
                    items = json.loads(m.group(1))
                    for idx, item in enumerate(items):
                        if item.get("Value") == sv:
                            return str(idx)
                except (json.JSONDecodeError, KeyError):
                    pass
    return "0"


def _find_league_value(html_bytes: bytes, display_name: str) -> tuple[str, str]:
    """Return (value, index) for the league whose Text starts with display_name."""
    html = html_bytes.decode("windows-1254", errors="replace")
    soup = BeautifulSoup(html, "lxml")
    for script in soup.find_all("script"):
        text = script.string or ""
        if "cmbMacOrganizasyon" in text and "Initialize" in text:
            m = re.search(r",\s*(\[\{.*?\}\])\s*\)", text, re.DOTALL)
            if m:
                try:
                    items = json.loads(m.group(1))
                    for idx, item in enumerate(items):
                        if item.get("Text", "").startswith(display_name):
                            return item.get("Value", ""), str(idx)
                except (json.JSONDecodeError, KeyError):
                    pass
    return "", "-1"


def _build_form(state: dict, season: str, sv: str, si: str) -> dict:
    return {
        **state,
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__SCROLLPOSITIONX": "0",
        "__SCROLLPOSITIONY": "0",
        _SEL + "cmbSezon_text": season,
        _SEL + "cmbSezon_value": sv,
        _SEL + "cmbSezon_index": si,
        _SEL + "cmbMacOrganizasyon_text": "Seçiniz...",
        _SEL + "cmbMacOrganizasyon_value": "",
        _SEL + "cmbMacOrganizasyon_index": "-1",
        _SEL + "cmbGrup_text": "Seçiniz...",
        _SEL + "cmbGrup_value": "",
        _SEL + "cmbGrup_index": "-1",
        _SEL + "cmbKulup_text": "Seçiniz...",
        _SEL + "cmbKulup_value": "",
        _SEL + "cmbKulup_index": "-1",
        _SEL + "cmbCezaTuru_text": "Seçiniz...",
        _SEL + "cmbCezaTuru_value": "",
        _SEL + "cmbCezaTuru_index": "0",
        _SEL + "hdnSezonID": sv,
        _SEL + "hdnMacOrgID": "",
        _SEL + "hdnMacOrgGrupID": "",
        _PREFIX + "cmbKurul_text": "Tümü",
        _PREFIX + "cmbKurul_value": "",
        _PREFIX + "cmbKurul_index": "-1",
        _PREFIX + "cmbMuhattap_text": "Tümü",
        _PREFIX + "cmbMuhattap_value": "",
        _PREFIX + "cmbMuhattap_index": "-1",
        _PREFIX + "txtKulupAdi": "",
        _PREFIX + "cmbLigSelector$combo_text": "Seçiniz...",
        _PREFIX + "cmbLigSelector$combo_value": "",
        _PREFIX + "cmbLigSelector$combo_index": "0",
        _PREFIX + "cmbSezon$combo_text": season,
        _PREFIX + "cmbSezon$combo_value": sv,
        _PREFIX + "cmbSezon$combo_index": si,
        _PREFIX + "cmbOrganizasyon_text": "Tümü",
        _PREFIX + "cmbOrganizasyon_value": "",
        _PREFIX + "cmbOrganizasyon_index": "0",
        _PREFIX + "cmbFutbolcuSezon$combo_text": season,
        _PREFIX + "cmbFutbolcuSezon$combo_value": sv,
        _PREFIX + "cmbFutbolcuSezon$combo_index": si,
        _PREFIX + "cmbOrganizasyonAntr_text": "Tümü",
        _PREFIX + "cmbOrganizasyonAntr_value": "",
        _PREFIX + "cmbOrganizasyonAntr_index": "0",
        _PREFIX + "cmbFutbolcuSezonAntr$combo_text": season,
        _PREFIX + "cmbFutbolcuSezonAntr$combo_value": sv,
        _PREFIX + "cmbFutbolcuSezonAntr$combo_index": si,
        _PREFIX + "rmpCeza_Selected": "0",
    }


def _parse_penalty_table(html_bytes: bytes) -> list[PenaltyRecord]:
    soup = BeautifulSoup(html_bytes, "lxml")

    table = None
    for t in soup.find_all("table"):
        if t.find("th", class_="GridHeader_TFF_Contents"):
            table = t
            break

    if not table:
        return []

    tbody = table.find("tbody")
    if not tbody:
        return []

    records = []
    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 10:
            continue

        def cell(i: int) -> str:
            text = cols[i].get_text(strip=True)
            return "" if text == "\xa0" else text

        records.append(PenaltyRecord(
            license_no=cell(0),
            player_name=cell(1),
            penalty_match=cell(2),
            penalty_league=cell(3),
            penalty_group=cell(4) or None,
            suspension_match_date=cell(5),
            suspension_match=cell(6),
            suspension_league=cell(7),
            suspension_group=cell(8) or None,
            penalty_type=cell(9),
        ))

    return records


async def fetch_penalty_records(league_display_name: str, season: str) -> PenaltyResponse:
    sv = _season_value(season)

    async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT) as client:
        resp1 = await client.get(settings.CEZA_URL)
        resp1.raise_for_status()

        state1 = _extract_asp_state(resp1.content)
        si = _extract_season_index(resp1.content, sv)

        # Trigger season cascade to get updated league list for the requested season
        form2 = _build_form(state1, season, sv, si)
        form2["__EVENTTARGET"] = _SEL + "cmbSezon"
        form2["__EVENTARGUMENT"] = "TextChange"
        resp2 = await client.post(settings.CEZA_URL, data=form2)
        resp2.raise_for_status()

        state2 = _extract_asp_state(resp2.content)
        league_value, league_index = _find_league_value(resp2.content, league_display_name)

        if not league_value:
            raise Exception(
                f"League '{league_display_name}' not found for season {season}. "
                "It may not have been active in this season."
            )

        form3 = _build_form(state2, season, sv, si)
        form3[_SEL + "cmbMacOrganizasyon_text"] = league_display_name
        form3[_SEL + "cmbMacOrganizasyon_value"] = league_value
        form3[_SEL + "cmbMacOrganizasyon_index"] = league_index
        form3[_SEL + "hdnMacOrgID"] = league_value
        form3[_PREFIX + "btnSariKirmiziAra"] = "Ara"
        resp3 = await client.post(settings.CEZA_URL, data=form3)
        resp3.raise_for_status()

        records = _parse_penalty_table(resp3.content)

    return PenaltyResponse(
        league_name=league_display_name,
        season=season,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data=records,
    )

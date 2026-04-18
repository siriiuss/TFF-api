import pytest
from app.services.scraper import fetch_team_standings
from app.services.grouped_league_scraper import fetch_multi_group_standings

# Mark all tests in this file as asynchronous
pytestmark = pytest.mark.asyncio


async def test_super_league_scraping_logic():
    """Test if the scraper correctly parses the Trendyol Super League table."""
    # 198 is the pageID for Super League
    result = await fetch_team_standings("198")

    assert result.league_name is not None
    assert len(result.data) > 15  # Usually 19-20 teams
    assert result.data[0].rank == 1
    assert result.data[0].team_name != ""


async def test_multi_group_parsing():
    """Test if the grouped scraper handles 2. League properly."""
    # 976 is 2. League, index 0 is usually 'White Group'
    result = await fetch_multi_group_standings("976", group_index=0)

    assert "League ID: 976" in result.league_name
    assert len(result.data) > 0
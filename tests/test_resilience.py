import pytest
import respx
from httpx import Response, ReadTimeout
from app.services.scraper import fetch_team_standings
from app.services.grouped_league_scraper import fetch_multi_group_standings

# We use pytestmark to tell pytest that all tests in this file are async
pytestmark = pytest.mark.asyncio


@respx.mock
async def test_scraper_network_timeout():
    """
    Logic: Test the service function DIRECTLY.
    Verifies that a network timeout raises the specific English Exception used in the codebase.
    """
    # 1. Mock the TFF request to trigger a timeout
    respx.get(url__regex=r".*tff\.org.*").mock(
        side_effect=ReadTimeout("Connection Timed Out")
    )

    # 2. Call the service directly and expect an Exception
    with pytest.raises(Exception) as excinfo:
        await fetch_team_standings("198")

    # 3. Verify the error message matches the actual code
    assert "Error raised while connecting" in str(excinfo.value)


@respx.mock
async def test_scraper_invalid_html_structure():
    """
    Logic: Direct service test for unexpected HTML structure.
    Ensures the scraper raises an Exception when 's-table' is missing.
    """
    # 1. Mock TFF to return a valid page but without the standings table
    broken_html = "<html><body><div class='wrong-class'>No data here</div></body></html>"
    respx.get(url__regex=r".*tff\.org.*").mock(
        return_value=Response(200, content=broken_html)
    )

    # 2. Direct call
    with pytest.raises(Exception) as excinfo:
        await fetch_team_standings("198")

    # 3. Verify the exact error message (including the typo 'fint' in your current code)
    assert "failed to fint score table" in str(excinfo.value).lower()


@respx.mock
async def test_multi_group_scraper_index_error():
    """
    Logic: Direct test for multi-group logic when an invalid index is requested.
    """
    # Mock a minimal HTML with group links
    mock_html = '<a href="?grupID=1">Group A</a>'
    respx.get(url__regex=r".*tff\.org.*").mock(
        return_value=Response(200, content=mock_html)
    )

    # Requesting group index 5 (which doesn't exist in our mock_html)
    with pytest.raises(Exception) as excinfo:
        await fetch_multi_group_standings("976", group_index=5)

    # Checking for the newly added English translation
    assert "invalid group index" in str(excinfo.value).lower()
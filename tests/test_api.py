import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_health_check():
    """Verify the API is online and responding."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Online"


@pytest.mark.parametrize("league_name", settings.LEAGUES.keys())
def test_each_simple_league_endpoint(league_name):
    """Iterate through all simple leagues and verify they return 200 OK."""
    response = client.get(f"/api/standings/{league_name}")
    assert response.status_code == 200, f"Endpoint failed for league: {league_name}"

    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0


def test_invalid_league_name():
    """Verify that requesting a non-existent league returns a 404 error."""
    response = client.get("/api/standings/non-existent-league-123")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_multi_group_unsupported_endpoint():
    """Verify that multi-group leagues are blocked on the simple endpoint."""
    # Using a multi-group league key on a single-group endpoint
    league_key = "nesine-2-league"
    response = client.get(f"/api/standings/{league_key}")
    assert response.status_code == 400
    assert "multiple groups" in response.json()["detail"].lower()
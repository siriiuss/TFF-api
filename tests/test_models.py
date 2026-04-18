import pytest
from app.schemas.tff_models import TeamStanding
from pydantic import ValidationError

def test_team_standing_validation():
    """Ensure the Pydantic model rejects invalid data types."""
    # Points must be an integer. Providing a string should raise an error.
    with pytest.raises(ValidationError):
        TeamStanding(
            rank=1, team_name="Test", played=1, won=1, drawn=0,
            lost=0, goals_for=1, goals_against=0, goal_difference=1,
            points="INVALID_STRING"
        )
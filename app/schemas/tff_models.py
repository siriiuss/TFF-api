from pydantic import BaseModel, Field
from typing import List, Optional

class TeamStanding(BaseModel):
    rank: int = Field(..., alias="rank", description="The position of the team in the league table")
    team_name: str = Field(..., alias="team_name", description="The name of the football club")
    played: int = Field(..., alias="played", description="Total number of matches played")
    won: int = Field(..., alias="won", description="Number of matches won")
    drawn: int = Field(..., alias="drawn", description="Number of matches drawn")
    lost: int = Field(..., alias="lost", description="Number of matches lost")
    goals_for: int = Field(..., alias="goals_for", description="Total goals scored by the team")
    goals_against: int = Field(..., alias="goals_against", description="Total goals conceded by the team")
    goal_difference: int = Field(..., alias="goal_difference", description="Goal difference (goals_for - goals_against)")
    points: int = Field(..., alias="points", description="Total points earned")

    class Config:
        populate_by_name = True

class StandingsResponse(BaseModel):
    league_name: str = Field(default="Super League")
    season: str = Field(..., description="The season period (e.g., 2025-2026)")
    last_updated: str = Field(..., description="Timestamp of the last data update")
    data: List[TeamStanding]
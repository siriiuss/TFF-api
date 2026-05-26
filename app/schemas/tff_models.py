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


class PenaltyRecord(BaseModel):
    license_no: str = Field(..., description="Player license number")
    player_name: str = Field(..., description="Full name of the player")
    penalty_match: str = Field(..., description="Match in which the penalty was received")
    penalty_league: str = Field(..., description="League/organization in which the penalty was received")
    penalty_group: Optional[str] = Field(None, description="Group stage of the penalty match, if any")
    suspension_match_date: str = Field(..., description="Date of the match where suspension will be served")
    suspension_match: str = Field(..., description="Match where the suspension will be served")
    suspension_league: str = Field(..., description="League/organization where the suspension will be served")
    suspension_group: Optional[str] = Field(None, description="Group stage of the suspension match, if any")
    penalty_type: str = Field(..., description="Type of penalty (e.g. Kırmızı Kart, Sarı Kart, Men)")

    class Config:
        populate_by_name = True


class PenaltyResponse(BaseModel):
    league_name: str = Field(..., description="Name of the league queried")
    season: str = Field(..., description="The season period (e.g., 2025-2026)")
    last_updated: str = Field(..., description="Timestamp of the last data update")
    data: List[PenaltyRecord]

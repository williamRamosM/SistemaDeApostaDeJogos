from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class JogosModelSQL(SQLModel, table=True):
    
    __tablename__ = "jogos"

    id: Optional[int] = Field(default=None, primary_key=True)
    incremental_id: int
    team_one: int
    team_two: int
    date_game: datetime
    status: bool = Field(default=False)
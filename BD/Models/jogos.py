from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class Jogos(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)
    team_one: int
    team_two: int
    date_game: datetime
    status: bool = Field(default=False)
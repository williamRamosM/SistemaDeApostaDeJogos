from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class Bets(SQLModel, table=True):
   
    id: Optional[int] = Field(default=None, primary_key=True)
    points: Optional[Decimal] = None
    user_id: Optional[int] = Field(default=None, foreign_key="Usuarios.ID")
    game_id: Optional[int] = Field(default=None, foreign_key="Jogos.ID")
    odds: Optional[Decimal] = None
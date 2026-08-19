from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class JogosModel(SQLModel, table=True):
    
    __tablename__ = "jogos"

    id: Optional[int] = Field(default=None, primary_key=True)
    incremental_id: int
    team_one: int
    team_two: int
    placar_one: Optional[int] = None
    placar_two: Optional[int] = None
    date_game: datetime
    status: bool = Field(default=False)
    jogo_iniciado: bool = Field(default=False)
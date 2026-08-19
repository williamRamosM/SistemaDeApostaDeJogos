from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

from repositories.models.usuario import Usuario
from repositories.models.jogos import JogosModel

class BetsModel(SQLModel, table=True):

    __tablename__ = "bets"
   
    id: Optional[int] = Field(default=None, primary_key=True)
    points: Optional[Decimal] = None
    odds: Optional[Decimal] = None
    status: str = Field(default="pendente")
    time_escolhido_id: int
    user_id: Optional[int] = Field(default=None, foreign_key="public.usuarios.id")
    game_id: Optional[int] = Field(default=None, foreign_key="jogos.id")
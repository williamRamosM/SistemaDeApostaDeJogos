from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class Usuario(SQLModel, table=True):
    __tablename__ = "Usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)     
    name: str    
    email: str  
    cpf: str    
    date_birth: date
    login: str 
    passworld: str 
    points: Decimal = Field(default=Decimal("100"))

class Jogos(SQLModel, table=True):
    __tablename__ = "Jogos"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_one: int
    team_two: int
    date_game: datetime
    status: bool = Field(default=False)

class Bets(SQLModel, table=True):
    __tablename__ = "Bets"

    id: Optional[int] = Field(default=None, primary_key=True)
    points: Optional[Decimal] = None
    user_id: Optional[int] = Field(default=None, foreign_key="Usuarios.ID")
    game_id: Optional[int] = Field(default=None, foreign_key="Jogos.ID")
    odds: Optional[Decimal] = None
    
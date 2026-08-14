from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class Usuario(SQLModel, table=True):
    
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "public"}

    id: Optional[int] = Field(default=None, primary_key=True)   
    incremental_id: int = Field(default=1)
    name: str    
    email: str  
    cpf: str    
    date_birth: date
    login: str 
    password: str 
    points: Decimal = Field(default=Decimal("100"))
    status: bool = Field(default=True)
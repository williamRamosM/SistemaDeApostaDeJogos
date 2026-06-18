from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class Usuario(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)     
    name: str    
    email: str  
    cpf: str    
    date_birth: date
    login: str 
    passworld: str 
    points: Decimal = Field(default=Decimal("100"))
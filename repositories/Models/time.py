from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class TimeModel(SQLModel, table=True):
    
    __tablename__ = "times"

    id: Optional[int] = Field(default=None, primary_key=True)
    incremental_id: int
    name: str
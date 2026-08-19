from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JogoSchemas(BaseModel):
    incremental_id: int
    team_one: int
    team_two: int
    date_game: datetime
    status: bool = False
    status_game: bool = False

class JogoAtualizarSchemas(BaseModel):
    incremental_id: int
    date_game: datetime
    status: Optional[bool] = None
    status_game: Optional[bool] = None
    placar_one: Optional[int] = None
    placar_two: Optional[int] = None
    

from pydantic import BaseModel
from datetime import datetime

class JogoModel(BaseModel):
    incremental_id: int
    team_one: int
    team_two: int
    date_game: datetime
    status: bool = False
    

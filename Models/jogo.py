from pydantic import BaseModel
from datetime import datetime

class JogoModel(BaseModel):
    team_one: int
    team_two: int
    date_game: datetime
    status: bool = False
    

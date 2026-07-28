from pydantic import BaseModel

class ApostaModel(BaseModel):
    points: int
    user_id: int
    game_id: int
    odds: float
from pydantic import BaseModel

class ApostaSchemas(BaseModel):
    points: int
    user_id: int
    game_id: int
    time_escolhido_id: int
    status: str

class ApostaUsuarioSchemas(BaseModel):
    user_id: int
    points: int


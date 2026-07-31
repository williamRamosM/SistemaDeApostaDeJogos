from pydantic import BaseModel

class ApostaSchemas(BaseModel):
    points: int
    user_id: int
    game_id: int
    odds: float
    status: bool 

class ApostaCriarSchemas(BaseModel):
    game_id: int
    status: bool

class ApostaUsuarioSchemas(BaseModel):
    user_id: int
    points: int
    odds: float


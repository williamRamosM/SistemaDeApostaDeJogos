from pydantic import BaseModel
from datetime import date

class UsuarioModel(BaseModel):
    nome: str
    email: str 
    cpf: str
    data_nascimento: date
    login: str
    senha: str
    
class UsuarioSchemasForLogin(BaseModel):
    login: str
    senha: str
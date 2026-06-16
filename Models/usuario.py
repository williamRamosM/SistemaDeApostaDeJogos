from dataclasses import dataclass
from datetime import date

@dataclass
class Usuario:
    nome: str
    email: str 
    cpf: str
    data_nascimento: date
    login: str
    senha: str
    
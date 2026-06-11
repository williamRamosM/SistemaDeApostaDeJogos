from dataclasses import dataclass
from datetime import date
import re

@dataclass
class Usuario_DAO:

    nome: str
    email: str 
    cpf: str
    data_nascimento: date
    login: str
    senha: str

    def adicionar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        a=1

    def verificar_senha(self, senha):
        formula = r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$"
        if re.match(formula, senha):
            print("ok passa")
            return True
        else:
            print("Nao passa")
            return False
        
    def verificar_name_user(username):
        with open(r"DAO/names.txt", "r", encoding="utf-8") as arquivo:
            linha = arquivo.read().splitlines()
        for value in linha:
            if(username == value):
                return False

        return True
        
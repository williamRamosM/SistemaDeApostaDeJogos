from repositories.usuarioBD import UsuarioBD
from repositories.connectionBD import engine
from services.jogos import Jogos
from sqlmodel import Session

class Administrador:

    def __init__(self):
        self.jogo = Jogos()

    def mostrar_usuarios(self):
        with Session(engine) as session:
            banco = UsuarioBD(session=session)
            informacao = banco.encontrar_todos_usuarios()
            return informacao

    def mostrar_usuario_expecifico(self, cpf):
        with Session(engine) as session:
            banco = UsuarioBD(session=session)
            informacao = banco.encontrar_usuario(cpf=cpf)
            return informacao

   

  
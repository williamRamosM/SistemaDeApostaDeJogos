from sqlmodel import create_engine, Session, SQLModel
from repositories.connectionBD import engine
from repositories.Models.usuario import Usuario

class UsuarioBD:

    def __init__(self, session:Session):
        self.session = session

    def cadastrar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        
            user = Usuario(name=nome,email=email,cpf=cpf,date_birth=data_nascimento,login=login,password=senha)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            print("Add usuario!")
    
    def mostrar_usuario():
        a=1

    def atualizar_usuario():
        a=1

    def excluir_usuario():
        a=1



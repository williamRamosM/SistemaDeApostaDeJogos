from sqlmodel import Session, SQLModel, select
from repositories.connectionBD import engine
from repositories.Models.usuario import Usuario
from sqlalchemy.exc import IntegrityError

class UsuarioBD:

    def __init__(self, session:Session):
        self.session = session

    def cadastrar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        
            user = Usuario(name=nome,email=email,cpf=cpf,date_birth=data_nascimento,login=login,password=senha)
            try:
                self.session.add(user)
                self.session.commit()
                self.session.refresh(user)
                print("Add usuario!")
            except IntegrityError:
                 self.session.rollback()
                 raise ValueError("System > Encontramos uma tentativa de duplicado e foi neutralizado.")
    
    def buscar_usuario(self, login):
        user = self.session.get(Usuario, login)
        
        if not user:
             return False
        else:
             return True

    def atualizar_usuario(self, id, nome, email, cpf, data_nascimento, login, senha):
         a=1

    def excluir_usuario():
        a=1

    def credencial_login(self, login):
        user = select(Usuario).where(Usuario.login == login)
        return self.session.exec(user).first()



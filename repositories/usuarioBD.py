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

    def atualizar_usuario(self, id, nome, email, cpf, data_nascimento, login, senha):
         a=1

    def excluir_usuario(self, login):
        login_encontrado = select(Usuario).where(Usuario.login == login)
        user = self.session.exec(login_encontrado).first()
    
        if(not user):
             return False

        try:     
            user.status = False
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise ValueError("System > Encontramos um erro e foi neutralizado.")
        
        return True

    def credencial_login(self, login):
        user = select(Usuario).where(Usuario.login == login)
        return self.session.exec(user).first()

    # def mostrar_saldo(self, login):
    #     login_encontrado = select(Usuario).where(Usuario.login == login)
    #     user = self.session.exec(login_encontrado).first()
    
    #     if not user:
             


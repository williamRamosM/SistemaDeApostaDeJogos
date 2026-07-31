from sqlmodel import Session, SQLModel, select
from repositories.connectionBD import engine
from repositories.models.usuario import Usuario
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

    def atualizar_senha(self, login, new_senha):
        user = self.credencial_login(login=login)

        if not user:
            return False
    
        user.password = new_senha
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return True

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

    def capturar_saldo(self, login):
        user = self.credencial_login(login=login)

        if not user:
             return None
        
        return user.points

    def mostrar_usuario(self, cpf):
        user = select(Usuario).where(Usuario.cpf == cpf)
        dados = self.session.exec(user).first()

        lista = (
            dados.id,
            dados.name,
            dados.cpf,
            dados.date_birth,
            dados.email,
            dados.login,
            dados.points,
            dados.status
        )
        return lista

    
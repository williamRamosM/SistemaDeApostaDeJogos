from sqlmodel import Session, SQLModel, select
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

    def encontrar_usuario(self, cpf):
        user = select(Usuario).where(Usuario.cpf == cpf)
        dados = self.session.exec(user).first()

        if dados is not None:

            dicionario = {
                "Nivel de acesso - ": dados.incremental_id,
                "Nome - ": dados.name,
                "CPF - ": dados.cpf,
                "Email - ": dados.email,
                "Data -":  dados.date_birth,
                "Username [Login] -":dados.login,
                "Pontos -":dados.points,
                "Pode apotar -":dados.status,
            }
        else:
            dicionario = None
    
        return dicionario

    def encontrar_todos_usuarios(self):
        jogo = select(Usuario)
        dados = self.session.exec(jogo).all()
        lista = []
        for value in dados:
            dicionario = {
                "Nivel de acesso - ": value.incremental_id,
                "Nome - ": value.name,
                "CPF - ": value.cpf,
                "Email - ": value.email,
                "Data -":  value.date_birth,
                "Username [Login] -":value.login,
                "Pontos -":value.points,
                "Pode apotar -":value.status,
            }
            lista.append(dicionario)
        return lista

    def encontrar_indentificador(self, login):
        user = select(Usuario).where(Usuario.login == login)
        dados = self.session.exec(user).first()

        if dados is not None:
            return dados.incremental_id
        return None

    def encontrar_id(self, login):
            user = select(Usuario).where(Usuario.login == login)
            dados = self.session.exec(user).first()
    
            if dados is not None:
                return dados.id
            return None

    def encontrar_name(self, id):
        user = select(Usuario).where(Usuario.id == id)
        dados = self.session.exec(user).first()

        if dados is not None:
            return dados.login
        return None
    
    def atualizar_pontos_user(self, user_id, pontos, status):
        user = select(Usuario).where(Usuario.id == user_id)
        dados = self.session.exec(user).first()

        if status == True:
            dados.points += pontos
        else:
            dados.points -= pontos

        self.session.add(dados)
        self.session.commit()


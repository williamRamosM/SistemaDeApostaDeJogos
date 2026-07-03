from services.security_passworld import SecurityPassWorld
from services.security_username import SecurityUsername
from repositories.usuarioBD import UsuarioBD
from repositories.connectionBD import engine
from Models.usuario import UsuarioModelForLogin
from Models.usuario import UsuarioModel
from validate_docbr import CPF
from sqlmodel import Session
from datetime import date
import re

class Usuario:

    def adicionar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        usuario = UsuarioModel(nome=nome, email=email, cpf=cpf, data_nascimento=data_nascimento, login=login, senha=senha)
        #data_nascimento_tratado: date = data_nascimento
        validate_username = SecurityUsername()
        cript = SecurityPassWorld()
       
        if not(validate_username.verificar_username(username=usuario.nome)):
            raise TypeError("System > Usuario digitou um nome proibido!")

        if not(self._verificar_email(email=usuario.email)):
            raise TypeError("System > Usuario digitou um email invalido!")

        if not(self._verificar_cpf(cpf=usuario.cpf)):
            raise TypeError("System > Usuario digitou um CPF invalido!")
        
        if not(self._verificar_idade(data_nascimento=usuario.data_nascimento)):
            raise TypeError("System > Usuario possui uma idade inferior a 18 anos!")

        if not(validate_username.verificar_username(username=usuario.login)):
            raise TypeError("System > Usuario digitou um login proibido!")

        self._verificar_login(usuario.login)

        if not(self._verificar_senha(senha=usuario.senha)):
            raise TypeError("System > Usuario digitou uma senha invalida!")

        cpf_reformulado = self._formatacao_cpf(cpf=cpf)
        senha_cript = cript.codificar_senha(senha)

        with Session(engine) as session:
            banco = UsuarioBD(session)
            banco.cadastrar_usuario(
                nome=nome,
                email= email,
                cpf= cpf_reformulado,
                data_nascimento = data_nascimento,
                login= login,
                senha= senha_cript
            )

        return True
    
    def verificar_credencial(self, login, senha):
        cript = SecurityPassWorld()

        with Session(engine) as session:
            banco = UsuarioBD(session)
            user = banco.credencial_login(login=login)

            if user is None:
                raise TypeError("System > login ou senha invalidos")
            if not cript.autenticar_senha(password_salvo=user.password,passworld_atual=senha):
                raise TypeError("System > login ou senha invalidos")
            if not user.status:
                raise TypeError("System > Essa conta foi desativada!")
        return True
    
    def remover_usuario(self, login):
        with Session(engine) as session:
            banco = UsuarioBD(session)
            user = banco.excluir_usuario(login=login)

            if (not user):
                raise TypeError("System > Usuario nao existe!")
            
        return True

    def mostrar_pontos(self, login):
        with Session(engine) as session:
            banco = UsuarioBD(session=session)
            user = banco.capturar_saldo(login=login)

            if not user:
                raise ValueError("System > Usuario nao existe no sistema para poder mostrar o saldo!")
      
        return user

    def alterar_senha(self, login, new_senha, confirmar_senha):
        cript = SecurityPassWorld()
        usuario = UsuarioModelForLogin(login=login,senha=new_senha)

        if not self._confirmar_senha(password_one=new_senha, password_two=confirmar_senha):
            raise ValueError("System > as senhas digitadas nao sao identicas!")

        if not self._verificar_senha(senha=usuario.senha):
                    raise TypeError("System > Usuario digitou uma senha invalida!")
        
        senha = cript.codificar_senha(usuario.senha)
        with Session(engine) as session:
            banco = UsuarioBD(session=session)
            user = banco.atualizar_senha(login=usuario.login, new_senha=senha)

            if not user:
                raise TypeError("System > Usuario nao existe!")
            
            return True
# funçoes privadas.                        
    def _verificar_senha(self, senha):
        if(len(senha) != 8):
            return False
        
        formula = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^a-zA-Z0-9]).+$'
        
        if re.match(formula, senha):
            return True
        else:
            return False
        
    def _verificar_email(self, email):
        formula = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(formula, email):
            return True
        else:
            return False
        
    def _verificar_cpf(self, cpf):
        cpf_valide = CPF()

        if(len(cpf) != 11):
            return False
        if(cpf_valide.validate(cpf) == False):
            return False
        
        return True
       
    def _formatacao_cpf(self, cpf):
        new_cpf = re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4',cpf)
        return new_cpf

    def _verificar_login(self, login):

        with Session(engine) as session:
            banco = UsuarioBD(session)
            user = banco.credencial_login(login=login)

            if user is not None:
                raise TypeError("System > login ja registrado!")
            
        return True
    
    def _verificar_idade(self, data_nascimento):
        data_atual = date.today()
        ano_calculado = data_atual.year - data_nascimento.year

        if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
            ano_calculado -= 1

        if ano_calculado < 18:
            return False
        return True
    
    def _confirmar_senha(self, password_one, password_two):
        if password_one == password_two:
            return True
        else:
            return False


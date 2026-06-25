from services.security_passworld import SecurityPassWorld
from services.security_username import SecurityUsername
from repositories.usuarioBD import UsuarioBD
from repositories.connectionBD import engine
from Models.usuario import UsuarioModel
from validate_docbr import CPF
from sqlmodel import Session
from datetime import date
import re

class Usuario:

    def adicionar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        usuario = UsuarioModel(nome=nome, email=email, cpf=cpf, data_nascimento=data_nascimento, login=login, senha=senha)
        data_nascimento2: date = data_nascimento
        validate_username = SecurityUsername()
        cript = SecurityPassWorld()
       
        if not(validate_username.verificar_username(username=usuario.nome)):
            raise TypeError("System > Usuario digitou um nome proibido!")

        if not(self._verificar_email(email=usuario.email)):
            raise TypeError("System > Usuario digitou um email invalido!")

        if not(self._verificar_cpf(cpf=usuario.cpf)):
            raise TypeError("System > Usuario digitou um CPF invalido!")

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
                data_nascimento= data_nascimento2,
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
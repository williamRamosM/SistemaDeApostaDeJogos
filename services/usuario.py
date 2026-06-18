import re
from services.security_username import SecurityUsername
from Models.usuario import Usuario
from datetime import date

class Usuario:

    def adicionar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        
        validate = SecurityUsername()
        usuario = Usuario(nome=nome, email=email, cpf=cpf, data_nascimento=data_nascimento, login=login, senha=senha)

        data_nascimento2: date = data_nascimento
        
        if not(validate.verificar_username(username=usuario.nome)):
            TypeError("System > Usuario digitou um nome proibido!")

        if not(self.verificar_email(email=usuario.email)):
            TypeError("System > Usuario digitou um email invalido!")

        if not(self.verificar_cpf(cpf=usuario.cpf)):
            TypeError("System > Usuario digitou um CPF invalido!")

        if not(validate.verificar_username(username=usuario.login)):
            TypeError("System > Usuario digitou um login proibido!")

        if not(self.verificar_senha(senha=usuario.senha)):
            TypeError("System > Usuario digitou uma senha invalida!")

        return {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "data_nascimento": data_nascimento2,
            "login": login,
            "senha": senha  
        }
                            
    def verificar_senha(self, senha):
        formula = r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$'
        if re.match(formula, senha):
            return True
        else:
            return False
        
    def verificar_email(self, email):
        formula = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(formula, email):
            return True
        else:
            return False
        
    def verificar_cpf(self, cpf):
        if(len(cpf) == 11):
             formula = r'(\d{3})(\d{3})(\d{3})(\d{2})'
             if re.match(formula, cpf):
                return True
             else:
                return False
             
    def formatacao_cpf(self, cpf):
        new_cpf = re.sub(r'\1.\2.\3-\4', cpf)
        return new_cpf

        

        
        
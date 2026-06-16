import re
from Models.security_username import SecurityUsername
from datetime import date

class UsuarioDAO:

    def adicionar_usuario(self, nome, email, cpf, data_nascimento, login, senha):
        name = SecurityUsername().rescrever_username(nome)
        self.nome = _name = SecurityUsername.verificar_username(name)
        namelogin = SecurityUsername().rescrever_username(login)
        self.nome = _namelogin = SecurityUsername.verificar_username(namelogin)
        self.data_nascimento: date = data_nascimento
        
        if not(_name):
            TypeError("System > Usuario digitou um nome proibido!")
        if not(self.verificar_email(email=email)):
            TypeError("System > Usuario digitou um email invalido!")
        if not(self.verificar_cpf(cpf=cpf)):
            TypeError("System > Usuario digitou um CPF invalido!")
        if not(_namelogin):
            TypeError("System > Usuario digitou um nome proibido!") 
        if not(self.verificar_senha(senha=senha)):
            TypeError("System > Usuario digitou uma senha invalida!")

        return {
            "nome": _name,
            "email": email,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "login": _namelogin,
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

        

        
        
from DAO import usuario_dao
from Models import security_username

usuario = security_username.Security_Username()
nome = "usuario01"
name = usuario.rescrever_username(nome)
if usuario.verificar_username(name) == True:
    print("Bem vindo(a)")
else:
    print("Recusado conection")

from services.usuario import Usuario
from datetime import date

user = Usuario()

nome = "william"
email = "test@gmail.com"
cpff = "04809811085"
data = date(2006,10,3)
nameUser = "william"
senhaa = "wiLL1@Mm"

# try:
#     print(user.adicionar_usuario(nome=nome,email=email,cpf=cpff,data_nascimento=data,login=nameUser,senha=senhaa))
# except TypeError as e:
#     print(e)

status = True
while status != False:

    a=1

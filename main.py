from services.usuario import Usuario
from datetime import date
user = Usuario()

nome = "william"
email = "test@gmail.com"
cpf = "04809811085"
data = date(2006,10,3)
login = "william"
senha = "wiLL1@Mm"

def sing_up_user():
    status_sing = True
    status_conta = True
   
    while status_sing != False:
        nome = input("Digite [Nome] > ")
        email = input("Digite [E-mail] > ")
        cpf = input("Digite [CPF] > ")

        print(">> Informe a sua data de nascimento abaixo nesse parametro (AAAA/MM/DD) <<")
        dia = int(input("Digite [dia] > "))
        mes = int(input("Digite [mes] > "))
        ano = int(input("Digite [ano] > "))
        
        print(">> Crie um login e senha para a conta <<")
        login = input("Digite [username] > ")
        senha = input("Digite [senha] > ")

        try:
           data = date(year=ano,month=mes,day=dia)
           if user.adicionar_usuario(nome=nome,email=email,cpf=cpf,data_nascimento=data,login=login,senha=senha):
               status_sing = False
        except TypeError as e:
            print(e)

    raise ValueError("System > Faça login com a sua conta para acessar!")

def login_user():
    status = False
    status_conta = True
    while status_conta != False:
        login = input("Digite [username] > ")
        senha = input("Digite [senha] > ")
        try:
            if(user.verificar_credencial(login=login, senha=senha)):
                status = True
                status_conta = False
    
        except TypeError as e:
            print(e)

        status_confirmar = True
        while status_confirmar != False:
            print("Tentar denovo? Y/N")
            escolha = input(">").lower()
            try:
                if escolha ==  "y":
                    raise ValueError("System > Tentando novamente!")
                elif escolha == "n":
                    status_conta = False
                    status_confirmar = False
            except ValueError as e:
                print(e)

    return status

def inicial_acesso():
    status = True
    while status != False:
        print("sing up [1] - login [2]")
        escolha = input("Digite > ")

        try:
            match(escolha):
                case "1":
                    sing_up_user()
                case "2":
                    if login_user():
                        status = False
                case _:
                    raise ValueError("System > Opcao invalida!")
        except ValueError as e:
            print(e)
        

# try:
#     print(user.adicionar_usuario(nome=nome,email=email,cpf=cpff,data_nascimento=data,login=nameUser,senha=senhaa))
# except TypeError as e:
#     print(e)

if __name__ == "__main__":
    inicial_acesso()
    print("ok acessou... hacker!!")

    

    
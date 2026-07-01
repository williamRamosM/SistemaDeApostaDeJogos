from services.usuario import Usuario
from datetime import date
user = Usuario()

# nome = "william"
# email = "test@gmail.com"
# cpf = "04809811085"
# data = date(2006,10,3)
# login = "william"
# senha = "wiLL1@Mm"

menu_tuple = ("Sair", "Status da minha aposta", "Multiplicar a aposta", "Cancelar minha participação nas apostas","Trocar a senha","Resultados de jogos anteriores de uma seleção ","Apostas ativas","Saldo de pontos","Ver o ranking de apostadores")

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
    login = ""
    while status_conta != False:
        status_confirmar = True
        login = input("Digite [username] > ")
        senha = input("Digite [senha] > ")
        try:
            if(user.verificar_credencial(login=login, senha=senha)):
                status = True
                status_confirmar = False
                status_conta = False
    
        except TypeError as e:
            print(e)

        while status_confirmar != False:
            print("Tentar denovo? Y/N")
            escolha = input(">").lower()
            try:
                if escolha ==  "y":
                    status_confirmar = False
                    raise ValueError("System > Tentando novamente!")
                elif escolha == "n":
                    status_conta = False
                    status_confirmar = False
            except ValueError as e:
                print(e)

    return status, login

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
                    login_status, login = login_user()
                    if login_status:
                        status = False
                case _:
                    raise ValueError("System > Opcao invalida!")
        except ValueError as e:
            print(e)
    return login
        
def sair_aposta(username):  
    status = True
    status_permanecer_no_programa = True
    op = ""
    escolha = ""
    while status != False:
        status_confirmar = True
        print("System > Logo abaixo coloque a sua senha para confirmar que realmente eh voce!")
        senha = input("Digite [Senha] > ")
        try:
            if(user.verificar_credencial(login=username,senha=senha)):
               
                    op = input("System > Quer realmente sair do sistema? (Y/N) > ")
                    if op ==  "y":

                        if(user.remover_usuario(login=username)):
                            status_permanecer_no_programa = False
                            status = False
                            status_confirmar = False
                            raise ValueError("System > Usuario removido do sistema!")
                    elif op == "n":
                        status = False
                        status_confirmar = False
        except TypeError as e:
            print(e)
        except ValueError as e:
            print(e)

        while status_confirmar != False:
            escolha = input("System > Tentar denovo? (Y/N) >").lower()
            try:
                if escolha ==  "y":
                    status_confirmar = False
                    raise ValueError("System > Tentando novamente!")
                elif escolha == "n":
                    status = False
                    status_confirmar = False
            except ValueError as e:
                print(e)
    return status_permanecer_no_programa

def listar_menu(componente):
    for i, value in enumerate(componente):
        print("[",i,"]", value)

# try:
#     print(user.adicionar_usuario(nome=nome,email=email,cpf=cpff,data_nascimento=data,login=nameUser,senha=senhaa))
# except TypeError as e:
#     print(e)

username = inicial_acesso()
status = True
op = "0"
while(status != False):
    listar_menu(componente=menu_tuple)
    try:
        op = input("Digite > ")
        match(op):
            case "0":
                status = False
            case "1":
                raise ValueError("System > Em breve tera algo aqui!")
            case "2":
                raise ValueError("System > Em breve tera algo aqui!")
            case "3":
                status = sair_aposta(username=username)
            case "4":
                raise ValueError("System > Em breve tera algo aqui!")
            case "5":
                raise ValueError("System > Em breve tera algo aqui!")
            case "6":
                raise ValueError("System > Em breve tera algo aqui!")
            case "7":
                raise ValueError("System > Em breve tera algo aqui!")
            case _:
                raise ValueError("System > Exprecao invalida")    

    except ValueError as e:
        print(e)
from services.usuario import Usuario
from services.administrador import Administrador
from services.jogos import Jogos
from datetime import date

class Compilar:

    def __init__(self):
        self.user = Usuario()
        self.administrador = Administrador()
        self.jogo = Jogos()
        self.menu_tuple = ("Sair", "Status da minha aposta", "Multiplicar a aposta", "Cancelar minha participação nas apostas","Trocar a senha","Resultados de jogos anteriores de uma seleção ","Apostas ativas","Saldo de pontos","Ver o ranking de apostadores")
        self.menu_tupleAdmin = ("Sair", "Ver dados de usuarios", "Ver dados de um usuario", "Ver dados de aposta de uma partida","Criar uma aposta","Ver o ranking de apostadores")

    def criar_aposta_admin(self):
        status = False
        status2 = False
        valor = ""
        while status != True:
            try:
                valor = self._auxiliar_escolha_admin()
                if self.jogo.buscar_existencia_jogo(id=valor):
                    status = True 
                else:
                    raise ValueError("System > Nao foi encontrado, confira se digitou corretamente!")
            except ValueError as e:
                print(e)
        while status2 != True:
            try: 
                print("[1] - True \n" \
                "[2] - False")
                escolha = int(input("Digite >"))

                match(escolha):
                    case 1:
                        self.jogo.ativar_jogo(id=valor)
                        status2 = True
                    case 2:
                        status2 = True
                    case _:
                        raise ValueError("System > A opcao escolhida nao existe!")
            except ValueError as e:
                print(e)

    def _auxiliar_escolha_admin(self):
        dado = self.jogo.buscar_jogos()
        for value, jogo in enumerate(dado):
            print("[",value + 1,"]", jogo['Jogo_Times'], jogo['Data'])
        try:
            num = int(input("Digite >"))

            if(num > len(dado) or num < 1):
                raise ValueError("System > Desculpe mas a opcao escolhida nao existe!")

            jogo = dado[num-1]
        except ValueError as e:
            print(e)
            
        return jogo["ID"]

    def _procurar_usuario(self):
        cpf = input("digite [CPF] >")
        value = self.administrador.mostrar_usuario_expecifico(cpf=cpf)
        if(value is not None):
            print(value)
        else:
            raise ValueError("System > Nao foi possivel encontrar o usuario com esse CPF!")

    def _sing_up_user(self):
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
                if self.user.adicionar_usuario(nome=nome,email=email,cpf=cpf,data_nascimento=data,login=login,senha=senha):
                    status_sing = False
            except TypeError as e:
                print(e)

        raise ValueError("System > Faça login com a sua conta para acessar!")

    def _login_user(self):
        status = False
        status_conta = True
        login = ""
        num = 0
        while status_conta != False:
            status_confirmar = True
            login = input("Digite [username] > ")
            senha = input("Digite [senha] > ")
            try:
                if(self.user.verificar_credencial(login=login, senha=senha)):
                    num = self.user.mostrar_indentificador(login=login)
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

        return status, login, num

    def _trocar_senha(self, username):
        status = True
        op = ""
        escolha = ""
        while status != False:
            status_confirmar = True
            print("System > Logo abaixo coloque a sua senha para confirmar que realmente eh voce!")
            senha = input("Digite [Senha] > ")
            try:
                if(self.user.verificar_credencial(login=username,senha=senha)):
                
                    senha_one = input("Digite [Nova Senha] > ")
                    senha_two = input("Digite [Confirme Senha] > ")
                    op = input("System > Quer realmente trocar a senha? (Y/N) > ")
                    if op ==  "y":

                        if(self.user.alterar_senha(login=username, new_senha=senha_one,confirmar_senha=senha_two)):
                            status = False
                            status_confirmar = False
                            raise ValueError("System > senha foi modificada!")
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

    def inicial_acesso(self):
        status = True
        while status != False:
            print("sing up [1] - login [2]")
            escolha = input("Digite > ")

            try:
                match(escolha):
                    case "1":
                        self._sing_up_user()
                    case "2":
                        login_status,login,num = self._login_user()
                        if login_status:
                            status = False
                    case _:
                        raise ValueError("System > Opcao invalida!")
            except ValueError as e:
                print(e)
        
        self._menu(num=num, login=login)

    def _sair_aposta(self, username):  
        status = True
        status_permanecer_no_programa = True
        op = ""
        escolha = ""
        while status != False:
            status_confirmar = True
            print("System > Logo abaixo coloque a sua senha para confirmar que realmente eh voce!")
            senha = input("Digite [Senha] > ")
            try:
                if(self.user.verificar_credencial(login=username,senha=senha)):
                
                        op = input("System > Quer realmente sair do sistema? (Y/N) > ")
                        if op ==  "y":

                            if(self.user.remover_usuario(login=username)):
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

    def _listar_menu(self, componente):
        for i, value in enumerate(componente):
            print("[",i,"]", value)

    def _menu(self, num, login):
        status = True

        match(num):
            case 1:
                print("System > Voce esta em uma conta de CLIENTE")
                while(status != False):
                    self._listar_menu(componente=self.menu_tuple)
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
                                status = self._sair_aposta(username=login)
                            case "4":
                                self._trocar_senha(username=login)
                            case "5":
                                raise ValueError("System > Em breve tera algo aqui!")
                            case "6":
                                raise ValueError("System > Em breve tera algo aqui!")
                            case "7":
                                print("Pontos [saldo] > ",self.user.mostrar_pontos(login=login))
                            case "8":
                                raise ValueError("System > Em breve tera algo aqui!")
                            case _:
                                raise ValueError("System > Exprecao invalida")    

                    except ValueError as e:
                        print(e)
            case 2:
                print("System > Voce esta em uma conta de ADMIN")
                while(status != False):
                    self._listar_menu(componente=self.menu_tupleAdmin)
                    try:
                        op = input("Digite > ")
                        match(op):
                            case "0":
                                status = False
                            case "1":
                                print(self.administrador.mostrar_usuarios())
                            case "2":
                                self._procurar_usuario()
                            case "3":
                                raise ValueError("System > Em breve tera algo aqui!")
                            case "4":
                                print("gg")
                            case "5":
                                raise ValueError("System > Em breve tera algo aqui!")
                            case _:
                                raise ValueError("System > Exprecao invalida")    

                    except ValueError as e:
                        print(e)


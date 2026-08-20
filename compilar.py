from services.usuario import Usuario
from services.administrador import Administrador
from services.aposta import Aposta
from services.jogos import Jogos
from services.time import Time
from datetime import date

class Compilar:

    def __init__(self):
        self.user = Usuario()
        self.aposta = Aposta()
        self.administrador = Administrador()
        self.jogo = Jogos()
        self.time = Time()
        self.menu_tuple = ("Sair", "Status da minha aposta", "Multiplicar a aposta", "Cancelar minha participação nas apostas","Trocar a senha","Resultados de jogos anteriores de uma seleção ","Apostas ativas","Saldo de pontos","Ver o ranking de apostadores","Registrar uma aposta")
        self.menu_tupleAdmin = ("Sair", "Ver dados de usuarios", "Ver dados de um usuario", "Ver dados de aposta de uma partida","Criar uma aposta","Ver o ranking de apostadores")

    def _criar_aposta_admin(self):
        status = False
        status2 = False
        valor = ""
        while status != True:
            try:
                valor = self._auxiliar_escolha(status=False)
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
                        print(self.jogo.ativar_jogo(id=valor))
                        status2 = True
                    case 2:
                        status2 = True
                    case _:
                        raise ValueError("System > A opcao escolhida nao existe!")
            except ValueError as e:
                print(e)

    def _mostrar_classificacao(self):
        dado = self.aposta.montar_classificacao_users()
        for dados in dado:
            print(dados['posicao']," - ","Nome:", dados['user'],"Acerto(s): ", dados['acerto'])

    def _mostrar_informacoes_jogo_expecifico(self):
        dado = self.jogo.buscar_jogos(status=True)
        if len(dado) == 0:
            raise ValueError("System > nao tem como ver algo que nao existe, desculpe.")
        try:
            value = self._auxiliar_escolha(status=True)
            dados = self.administrador.mostrar_infors_partida(game_id=value)
            print("Time da casa",dados["time1"], "Apostadores do time da casa:", dados["qtd_apostadores1"], "ODDs desse time:", dados["odds1"], "Time de fora",dados["time2"], "Apostadores do time de fora:", dados["qtd_apostadores2"], "ODDs desse time:", dados["odds2"])
        except ValueError as e:
            print(e)

    def _apostar_user(self, user):
        carteira_pontos = self.user.mostrar_pontos(login=user)
        user_id = self.user.mostrar_id(login=user)
        status = False
        status2 = False
        status3 = False
        valor = ""
        pontos_escolhidos = 0
        escolhido_id = 0
        dado = self.jogo.buscar_jogos(status=True)
        if len(dado) == 0:
            raise ValueError("System > Desculpe, mas nao tem jogos!")
        else:
            while status != True:
                try:
                    valor = self._auxiliar_escolha(status=True)
                    if self.jogo.buscar_existencia_jogo(id=valor):
                        status = True 
                    else:
                        raise ValueError("System > Nao foi encontrado, confira se digitou corretamente!")
                except ValueError as e:
                    print(e)
            jogo_id = self.jogo.mostrar_id(id=valor)
            dados_aposta = self.aposta.capturar_informacao_aposta(user_id=user_id, game_id=jogo_id)
            if dados_aposta is not None:
                carteira_pontos += dados_aposta["pontos_apostados"]

            while status2 != True:
                try: 
                    dado = self.jogo.buscar_times(id=valor)
                    for value, team in enumerate(dado):
                        print("[",value + 1,"]", team)

                    num = int(input("Digite [Quem ganha?] >"))
                    
                    if(num > len(dado) or num < 1):
                        raise ValueError("System > Desculpe mas a opcao escolhida nao existe!")
                    
                    escolhido_id = dado[num-1]
                    status2 = True
                except ValueError as e:
                    print(e)

            while status3 != True:
                try: 
                    num = int(input("Digite [Pontos] >"))
                    if num <= 0:
                        raise ValueError("System > O valor informado nao eh considerado valido para o sistema!")
                    calculo = carteira_pontos - num
                    if(calculo < 0):
                        raise ValueError("System > Desculpe mas voce nao possui tantos pontos para apostar!")
                    pontos_escolhidos = num
                    status3 = True
                except ValueError as e:
                    print(e)

            if dados_aposta is not None:
                self.user.controlar_pontos(user_id=user_id, pontos=dados_aposta["pontos_apostados"], status=True)

            self.aposta.fazer_aposta(user=user_id, jogo_id=jogo_id, time_id=escolhido_id, pontos=pontos_escolhidos)
            self.user.controlar_pontos(user_id=user_id, pontos=pontos_escolhidos, status=False)
            print("Feito!")
        
    def _auxiliar_escolha(self, status):
        dado = self.jogo.buscar_jogos(status=status)
        for value, jogo in enumerate(dado):
            print("[", value + 1, "]", jogo['Jogo_Times'], jogo['Data'])
        
        num = int(input("Digite >"))

        if num > len(dado) or num < 1:
            raise ValueError("System > Desculpe mas a opcao escolhida nao existe!")

        escolhido_id = dado[num - 1]
        return escolhido_id["ID"]

    def _auxiliar_mostrar_aposta(self, user):
        user_id = self.user.mostrar_id(login=user)
        dado = self.aposta.mostrar_apostas_id(user_id=user_id)
        for dados in dado:
            print("Time: ",dados['time_escolhido'],"Pontos apostados: ", dados['pontos_apostados'],"Status: ", dados['status'])

    def _auxiliar_mostrar_apostas_ativas(self):
        dados = self.aposta.montar_aposta()
        for value in dados:
            print("Jogo: ", value['jogo_id'],"Data: ", value['data'], "Time 1:",value['team_one'], "ODD Time 1:",value['tupla_odd1'], "Time 2: ",value['team_two'],"ODD Time 2: ",value['tupla_odd2'])

    def _auxiliar_multiplicar_aposta(self, user_login):
        user_id = self.user.mostrar_id(login=user_login)
        dado = self.aposta.mostrar_apostas(user_id=user_id, status="pendente")

        if len(dado) == 0:
            raise ValueError("System > Desculpe mas voce nao possui nenhum aposta ativa ainda!")    
        
        for value, dados in enumerate(dado):
            print("[",value+1,"] Time: ",dados['time_escolhido'],"Pontos apostados: ", dados['pontos_apostados'],"Status: ", dados['status'])

        num = int(input("Digite [Qual a aposta?] >"))

        if(num > len(dado) or num < 1):
            raise ValueError("System > Desculpe mas a opcao escolhida nao existe!")
        
        escolhido_id = dado[num-1]
        id = escolhido_id["id"]
        num_qtd = int(input("Digite [Quanto vai multiplicar?] >"))
        self.aposta.aumentar_aposta(qtd=num_qtd,user_id=user_id,game_id=id)

    def _auxiliar_mostrar_times(self):
        dado_time = self.time.mostrar_times()
        
        for value, dados_time in enumerate(dado_time):
            print("[", value+1,"] Time: ",dados_time['nome'])
        num = int(input("Digite [Qual a aposta?] >"))
        
        if(num > len(dado_time) or num < 1):
            raise ValueError("System > Desculpe mas a opcao escolhida nao existe!")
        
        escolhido_id = dado_time[num-1]
        id_time = escolhido_id["id_incremental"]

        dado = self.jogo.mostrar_jogo_time(id_time=id_time)

        if(len(dado) == 0):
            raise ValueError("System > nao temos noticias ainda!")
        
        for dados in dado:
            print("Data: ",dados['data'],"Time 1: ", dados['team_one'],"gols: ", dados['placar_one'], "Time 2:",dados['team_two'],"gols: ", dados['placar_two'])
            
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
        status_ficar = True
        num = None
        login = None
        while status != False:
            print("Sair [0] - Sing up [1] - Login [2]")
            escolha = input("Digite > ")

            try:
                match(escolha):
                    case "0":
                        status = False
                        status_ficar = False
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
        
        self._menu(num=num, login=login, status=status_ficar)

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

    def _menu(self, num:None, login:None, status):
    
        match(num):
            case 1:
                print("System > Voce esta em uma conta de CLIENTE")
                while(status != False):
                    informacao = self.user.verificar_status_user(login=login)
                    if informacao is not False:
                        self._listar_menu(componente=self.menu_tuple)
                        try:
                            op = input("Digite > ")
                            match(op):
                                case "0":
                                    status = False
                                    self.inicial_acesso()
                                case "1":
                                    self._auxiliar_mostrar_aposta(user=login)
                                case "2":
                                    self._auxiliar_multiplicar_aposta(user_login=login)
                                case "3":
                                    status = self._sair_aposta(username=login)
                                case "4":
                                    self._trocar_senha(username=login)
                                case "5":
                                    self._auxiliar_mostrar_times()
                                case "6":
                                    self._auxiliar_mostrar_apostas_ativas()
                                case "7":
                                    print("Pontos [saldo] > ",self.user.mostrar_pontos(login=login))
                                case "8":
                                    self._mostrar_classificacao()
                                case "9":
                                    self._apostar_user(user=login)
                                case _:
                                    raise ValueError("System > Exprecao invalida")    

                        except ValueError as e:
                            print(e)
                    else:
                        raise ValueError("System > voce foi desconectado por nao ter pontos o suficiente!")
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
                                self._mostrar_informacoes_jogo_expecifico()
                            case "4":
                                self._criar_aposta_admin
                            case "5":
                                self._mostrar_classificacao()
                            case _:
                                raise ValueError("System > Exprecao invalida")    

                    except ValueError as e:
                        print(e)


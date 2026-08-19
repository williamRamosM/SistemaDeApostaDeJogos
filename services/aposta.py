from sqlmodel import Session
from repositories.connectionBD import engine
from repositories.betsBD import BetsBD
from repositories.jogoBD import JogoBD
from repositories.usuarioBD import UsuarioBD
from services.usuario import Usuario
from schemas.aposta import ApostaSchemas
from decimal import Decimal

class Aposta():

    def fazer_aposta(self, user, jogo_id, time_id, pontos):

        with Session(engine) as session:
            banco = BetsBD(session=session)
            aposta = ApostaSchemas(user_id=user, game_id=jogo_id, time_escolhido_id=time_id, points=pontos, status="pendente")

            banco.atualizar_aposta_status(
                user_id=aposta.user_id,
                game_id=aposta.game_id,
                status=aposta.status,
                new_status="substituida"
                
            )

            banco.cadastrar_aposta(
                user_id=aposta.user_id, 
                game_id=aposta.game_id, 
                time_id=aposta.time_escolhido_id,
                points=aposta.points, 
                status=aposta.status
            )
           
    def mostrar_apostas(self, user_id, status):
        with Session(engine) as session:
            banco = BetsBD(session=session)
            informacoes = banco.encontrar_apostas(user_id=user_id,status=status)
        return informacoes

    def calculo_odds(self, jogo_id, time_id, time_oposto_id, status):
        with Session(engine) as session:
            banco = BetsBD(session=session)
            qtd_time_atual =  banco.contagem_users_aposta(jogo_id, time_id, status=status)         
            qtd_time_oposto = banco.contagem_users_aposta(jogo_id, time_oposto_id, status=status)  
    
            if qtd_time_atual == 0:
                return 1.0
        return round(1 + (qtd_time_oposto / qtd_time_atual), 2)

    def montar_aposta(self):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            jogo = banco.buscar_jogos(status=True)

            lista = []
            for value in jogo:
                tupla_odd1 = self.calculo_odds(
                    jogo_id=value.id,
                    time_id=value.team_one,
                    time_oposto_id=value.team_two,
                    status="pendente"
                )
                tupla_odd2 = self.calculo_odds(
                    jogo_id=value.id,
                    time_id=value.team_two,
                    time_oposto_id=value.team_one,
                    status="pendente"
                )

                dicionario = {
                    "jogo_id": value.incremental_id,
                    "data": value.date_game,
                    "team_one": value.team_one,
                    "tupla_odd1": tupla_odd1,
                    "team_two": value.team_two,
                    "tupla_odd2": tupla_odd2,
                }
                lista.append(dicionario)

        return lista

    def aumentar_aposta(self, qtd, user_id, game_id):
        with Session(engine) as session:
            banco = BetsBD(session=session)
            pontos = banco.mostrar_pontos_apostado(user_id=user_id, game_id=game_id, status="pendente")
            if 1 >= qtd:
                raise ValueError("System > nao podemos multiplicar por esse valor!")
            resul = pontos * qtd
            if pontos > resul:
                raise ValueError("System > nao podemos multiplicar por que voce nao tem muitos pontos!", pontos, resul)

            banco.atualizar_aposta_pontos(
                user_id=user_id,
                game_id=game_id,
                status="pendente",
                new_points=resul)

    def finalizar_aposta(self, game_id, game_banco_id):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            banco2 = BetsBD(session=session)
            banco3 = UsuarioBD(session=session)
            lista = banco.mostrar_pontos_partida(id=game_id)
            lista2 = banco.mostrar_jogos_incremental(id=game_id)
            dado_jogo = banco.buscar_existencia(id=game_id)

            ponto_time1 = lista[0]
            ponto_time2 = lista[1]
            team_one = lista2[0]
            team_two = lista2[1]
            informacao = ""
            odd_final = 0
            id_ganhador = None
            if ponto_time1 is None or ponto_time2 is None:
                return

            if(ponto_time1 > ponto_time2):
                informacao = "time1"
            elif(ponto_time1 < ponto_time2):
                informacao = "time2"
            else:
                informacao = "empatado"
            
            dado = banco2.encontrar_apostas_status(game_id=game_banco_id, status="pendente")
            odd_final1 = self.calculo_odds(jogo_id=dado_jogo.id, time_id=team_one, time_oposto_id=team_two, status="pendente")
            odd_final2 = self.calculo_odds(jogo_id=dado_jogo.id, time_id=team_two, time_oposto_id=team_one, status="pendente")

            for dados in dado:
                if informacao == "empatado":
                    banco3.atualizar_pontos_user(dados.user_id, dados.points, status=True)
                    banco2.atualizar_aposta_status(user_id=dados.user_id, game_id=game_banco_id, status="pendente", new_status="empatado")
                    continue

                if informacao == "time1":
                    id_ganhador = team_one 
                else: 
                    id_ganhador = team_two
                
                if informacao == "time1":
                    odd_final = odd_final1 
                else:
                    odd_final = odd_final2

                if dados.time_escolhido_id == id_ganhador:
                    pontos = dados.points * Decimal(str(odd_final))
                    banco3.atualizar_pontos_user(dados.user_id, pontos, status=True)
                    banco2.atualizar_aposta_status(user_id=dados.user_id, game_id=game_banco_id, status="pendente", new_status="ganho")
                else:
                    banco2.atualizar_aposta_status(user_id=dados.user_id, game_id=game_banco_id, status="pendente", new_status="perdido")

    def montar_classificacao_users(self):
        with Session(engine) as session:
            banco = BetsBD(session=session)
            banco2 = UsuarioBD(session=session)

            lista = []
            dado = banco.contagem_aposta() 
            for value, dados in enumerate(dado):
                name = banco2.encontrar_name(id=dados[0])
                dicionario = {
                    "posicao": value+1,
                    "user": name,
                    "acerto": dados[1]
                }
                lista.append(dicionario)

            return lista



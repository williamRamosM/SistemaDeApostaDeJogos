from repositories.usuarioBD import UsuarioBD
from repositories.jogoBD import JogoBD
from repositories.betsBD import BetsBD
from repositories.timesBD import TimesBD
from repositories.connectionBD import engine
from services.jogos import Jogos
from services.aposta import Aposta

from sqlmodel import Session

class Administrador:

    def __init__(self):
        self.jogo = Jogos()

    def mostrar_usuarios(self):
        with Session(engine) as session:
            banco = UsuarioBD(session=session)
            informacao = banco.encontrar_todos_usuarios()
            return informacao

    def mostrar_usuario_expecifico(self, cpf):
        with Session(engine) as session:
            banco = UsuarioBD(session=session)
            informacao = banco.encontrar_usuario(cpf=cpf)
            return informacao

    def mostrar_infors_partida(self, game_id):
        with Session(engine) as session:
            bet = Aposta()
            banco_game = JogoBD(session=session)
            banco_bet = BetsBD(session=session)
            banco_team = TimesBD(session=session)

            jogo = banco_game.buscar_existencia(id=game_id)
            team_one = banco_bet.contagem_users_aposta(game_id=jogo.incremental_id, time_escolhido_id=jogo.team_one, status="pendente")
            team_two = banco_bet.contagem_users_aposta(game_id=jogo.incremental_id, time_escolhido_id=jogo.team_two, status="pendente")
            odd_team_one = bet.calculo_odds(jogo_id=jogo.id,time_id=jogo.team_one,time_oposto_id=jogo.team_two,status="pendente")
            odd_team_two = bet.calculo_odds(jogo_id=jogo.id,time_id=jogo.team_two,time_oposto_id=jogo.team_one,status="pendente")
            name_one = banco_team.encontrar_nome_times(incremental_id=jogo.team_one)
            name_two = banco_team.encontrar_nome_times(incremental_id=jogo.team_two)

            
            return{
                "time1":name_one,
                "qtd_apostadores1":team_one,
                "odds1":odd_team_one,
                "time2":name_two,
                "qtd_apostadores2":team_two,
                "odds2":odd_team_two,
            }


  
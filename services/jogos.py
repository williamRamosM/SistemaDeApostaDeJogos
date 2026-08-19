from api_services.api_generico import ApiGenerico
from schemas.jogo import JogoSchemas, JogoAtualizarSchemas
from sqlmodel import Session
from repositories.connectionBD import engine
from repositories.jogoBD import JogoBD
from services.aposta import Aposta

class Jogos():
    
    def sicronizar_dados_jogos(self):
        api = ApiGenerico()
        informacoes = api.encontrar_informacao(tipo="matches")

        with Session(engine) as session:
            banco = JogoBD(session=session)
            for dados in informacoes.get("matches", []):
                existe = banco.buscar_existencia(id = dados["id"])
                if existe:
                    continue

                jogo_schemas = JogoSchemas(incremental_id = dados["id"], team_one=  dados["homeTeam"]["id"], team_two=  dados["awayTeam"]["id"], date_game= dados["utcDate"], status= False, status_game=False)

                banco.registrar_jogo( 
                        incremental_id= jogo_schemas.incremental_id,
                        team_one= jogo_schemas.team_one,
                        team_two= jogo_schemas.team_two,
                        date_game=jogo_schemas.date_game,
                        status=jogo_schemas.status,
                        status_game=jogo_schemas.status_game
                    )

    def atualizar_dados(self):
        api = ApiGenerico()
        informacoes = api.encontrar_informacao(tipo="matches")
        with Session(engine) as session:
            banco = JogoBD(session=session)
            for dados in informacoes.get("matches", []):
                existe = banco.buscar_existencia(id=dados["id"]) 
                if not existe:
                    continue
                situacao = dados.get("status")
                lista = ("IN_PLAY", "FINISHED")
                new_date = None
                started = None
                new_status = None
                placar_one = None
                placar_two = None
                status_mudado = False

                if existe.date_game != dados["utcDate"]:
                    new_date = dados.get("utcDate")
                    status_mudado = True
                if situacao in lista and not existe.jogo_iniciado:
                    started = True
                    new_status = False
                    status_mudado = True  
                    
                if situacao == lista[1] and existe.placar_one is None:
                    placar_one = dados["score"]["fullTime"]["home"]
                    placar_two = dados["score"]["fullTime"]["away"]
                    status_mudado = True
                    
                if(status_mudado):
                    jogo_atualizar_schemas = JogoAtualizarSchemas(incremental_id= existe.incremental_id ,date_game= new_date, placar_one=placar_one, placar_two=placar_two, status=new_status, status_game=started)
                    banco.atualizar_jogo( 
                        incremental_id=jogo_atualizar_schemas.incremental_id,
                        date_game=jogo_atualizar_schemas.date_game,
                        status=jogo_atualizar_schemas.status,
                        jogo_iniciado=jogo_atualizar_schemas.status_game,
                        placar_one=jogo_atualizar_schemas.placar_one,
                        placar_two=jogo_atualizar_schemas.placar_two
                    )

                    if situacao == lista[1] and placar_one is not None:
                        aposta = Aposta()
                        aposta.finalizar_aposta(game_id=existe.incremental_id, game_banco_id=existe.id)
                    
    def buscar_jogos(self, status):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            informacoes = banco.mostrar_jogo(status=status)
        return informacoes

    def mostrar_id(self, id):
        with Session(engine) as session:
            banco = JogoBD(session=session)
        return banco.encontrar_id(incremental_id=id)

    def buscar_existencia_jogo(self, id):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            existencia = banco.buscar_existencia(id=id) 

            return existencia

    def ativar_jogo(self, id):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            banco.atualizar_status(incremental_id=id)
        return "Atualizado status!"

    def buscar_times(self, id):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            informacoes = banco.mostrar_jogos_incremental(id=id)
        return informacoes

    def mostrar_jogo_time(self, id_time):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            informacoes = banco.buscar_jogos_times(id_time=id_time)
        return informacoes
        
    
from api_services.api_generico import ApiGenerico
from schemas.jogo import JogoSchemas, JogoAtualizarSchemas
from sqlmodel import Session
from repositories.connectionBD import engine
from repositories.jogoBD import JogoBD

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

                jogo_schemas = JogoSchemas(incremental_id = dados["id"], team_one=  dados["homeTeam"]["id"], team_two=  dados["awayTeam"]["id"], date_game= dados["utcDate"], status= False)

                banco.registrar_jogo( 
                        incremental_id= jogo_schemas.incremental_id,
                        team_one= jogo_schemas.team_one,
                        team_two= jogo_schemas.team_two,
                        date_game=jogo_schemas.date_game,
                        status=jogo_schemas.status
                    )

    def atualizar_dodos(self):
        api = ApiGenerico()
        informacoes = api.encontrar_informacao(tipo="matches")
        with Session(engine) as session:
            banco = JogoBD(session=session)
            for dados in informacoes.get("matches", []):
                existe = banco.buscar_existencia(id=dados["id"]) 
                if not existe:
                    continue

                status = False
                if existe.date_game != dados["utcDate"]:
                    status = True

                if status:
                    jogo_atualizar_schemas = JogoAtualizarSchemas(incremental_id= existe.incremental_id ,date_game= dados["utcDate"])
                    banco.atualizar_jogo( 
                        incremental_id=jogo_atualizar_schemas.incremental_id,
                        date_game=jogo_atualizar_schemas.date_game
                    )

    def buscar_jogos(self):
        with Session(engine) as session:
            banco = JogoBD(session=session)
            informacoes = banco.mostrar_jogo(status=False)
        return informacoes

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

    def mostrar_jogo_usuario(self):
        with Session(engine) as session:
            try:
                banco = JogoBD(session=session)
                informacoes = banco.mostrar_jogo(status=True)
            except ValueError as e:
                print(e)
        return informacoes

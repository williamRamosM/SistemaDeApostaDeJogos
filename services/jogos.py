from api_services.api_generico import ApiGenerico
from Models.jogo import JogoModel
from sqlmodel import Session
from repositories.connectionBD import engine
from repositories.jogoBD import JogoBD
from repositories.Models.jogos import JogosModelSQL

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

                jogo_model = JogoModel( 
                    incremental_id = dados["id"],
                    team_one=  dados["homeTeam"]["id"],
                    team_two=  dados["awayTeam"]["id"],
                    date_game= dados["utcDate"],
                    status= False,
                )
                jogo = JogosModelSQL(**jogo_model.model_dump())

                banco.registrar_jogo(jogo=jogo)



from api_services.api_generico import ApiGenerico
from Models.jogo import JogoModel
from sqlmodel import Session
from repositories.connectionBD import engine

class Jogos():
    
    def sicronizar_dados_jogos(self):
        api = ApiGenerico()
        informacoes = api.encontrar_informacao(tipo="matches")

        list_jogos = []

        for dados in informacoes.get("matches", []):
            jogo = JogoModel( 
                team_one=  dados["homeTeam"]["id"],
                team_two=  dados["awayTeam"]["id"],
                date_game= dados["utcDate"],
                status= False,
            )
        
            list_jogos.append(jogo)

        return list_jogos


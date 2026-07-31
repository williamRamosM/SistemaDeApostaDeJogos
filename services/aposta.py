from sqlmodel import Session
from repositories.connectionBD import engine
from services.jogos import Jogos
from schemas.aposta import ApostaCriarSchemas

def criar_aposta(self, status, jogo_id):
    aposta = ApostaCriarSchemas(status=status, jogo_id=jogo_id)
    
def _auxiliar_criacao_aposta(self):
    status = False
    while status != True:
        Jogos.buscar_jogos()
        valor = int(input("Digite [ID do jogo] >"))

    if 

    

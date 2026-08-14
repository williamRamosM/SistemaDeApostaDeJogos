from sqlmodel import Session
from repositories.connectionBD import engine
from services.jogos import Jogos
from schemas.aposta import ApostaSchemas

class Aposta():
    def fazer_aposta(self, user, jogo_id):
       with Session(engine) as session:
           
   
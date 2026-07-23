from sqlmodel import Session, SQLModel, select
from repositories.connectionBD import engine
from repositories.Models.jogos import JogosModelSQL
from sqlalchemy.exc import IntegrityError
from Models.jogo import JogoModel

class JogoBD:
    def __init__(self, session:Session):
        self.session = session

    def registrar_jogo(self, incremental_id, team_one, team_two, date_game):
        jogo = JogosModelSQL(incremental_id=incremental_id, team_one=team_one, team_two=team_two, date_game=date_game)
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)
        
    def buscar_existencia(self, id):
        informacao = select(JogosModelSQL).where(JogosModelSQL.incremental_id == id)
        return self.session.exec(informacao).first()
        
    def atualizar_jogo(self, incremental_id, date_game):
        
        jogo = self.buscar_existencia(id=incremental_id)
        jogo.date_game = date_game
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)

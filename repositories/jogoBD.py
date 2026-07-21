from sqlmodel import Session, SQLModel, select
from repositories.connectionBD import engine
from repositories.Models.jogos import JogosModelSQL
from sqlalchemy.exc import IntegrityError
from Models.jogo import JogoModel

class JogoBD:
    def __init__(self, session:Session):
        self.session = session

    def registrar_jogo(self, jogo:JogosModelSQL):
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)
        
    def buscar_existencia(self, id):
        informacao = select(JogosModelSQL).where(JogosModelSQL.incremental_id == id)
        return self.session.exec(informacao).first()
        
    def atualizar_jogo(self, jogo_atualizado: JogosModelSQL):
        self.session.add(jogo_atualizado)
        self.session.commit()
        self.session.refresh(jogo_atualizado)

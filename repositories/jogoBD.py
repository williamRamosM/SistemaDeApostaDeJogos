from sqlmodel import Session, SQLModel, select
from repositories.connectionBD import engine
from repositories.models.jogos import JogosModel
from sqlalchemy.exc import IntegrityError

class JogoBD:
    def __init__(self, session:Session):
        self.session = session

    def registrar_jogo(self, incremental_id, team_one, team_two, date_game, status):
        jogo = JogosModel(incremental_id=incremental_id, team_one=team_one, team_two=team_two, date_game=date_game, status=status)
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)
        
    def buscar_existencia(self, id):
        informacao = select(JogosModel).where(JogosModel.incremental_id == id)
        return self.session.exec(informacao).first()
        
    def atualizar_jogo(self, incremental_id, date_game):
        jogo = self.buscar_existencia(id=incremental_id)
        jogo.date_game = date_game
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)

    def atualizar_status(self, incremental_id):
        jogo = self.buscar_existencia(id=incremental_id)
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)

    def mostrar_jogo(self, status):
        jogo = select(JogosModel)
        dados = self.session.exec(jogo).all()
        lista = []
    
       
        for value in dados:
            if(value.status == status):
                dicionario = {
                    "Jogo_Times": f'{value.team_one} VS {value.team_two}',
                    "Data": value.date_game,
                    "ID": value.incremental_id,
                    "Status": value.status
                }
                lista.append(dicionario)
        return lista
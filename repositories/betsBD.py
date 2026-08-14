from sqlmodel import Session, SQLModel, select
from repositories.models.bets import BetsModel
from sqlalchemy.exc import IntegrityError

class BetsBD:
    def __init__(self, session:Session):
        self.session = session

    def cadastrar_aposta_banco(self, points, user_id, game_id, odds, status):
        aposta = BetsModel(points=points, user_id=user_id, game_id=game_id, odds=odds, status=status)
        self.session.add(aposta)
        self.session.commit()
        self.session.refresh(aposta)

    

       
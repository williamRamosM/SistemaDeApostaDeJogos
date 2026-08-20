from sqlmodel import Session, SQLModel, select
from repositories.models.bets import BetsModel
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from repositories.models.usuario import Usuario
from repositories.models.jogos import JogosModel

class BetsBD:
    def __init__(self, session:Session):
        self.session = session

    def cadastrar_aposta(self, points, user_id, game_id, time_id, status):
        aposta = BetsModel(points=points, user_id=user_id, game_id=game_id, time_escolhido_id=time_id, status=status)
        self.session.add(aposta)
        self.session.commit()
        self.session.refresh(aposta)

    def buscar_aposta(self, user_id, game_id, status):
        bet = select(BetsModel).where(BetsModel.user_id == user_id, BetsModel.game_id == game_id, BetsModel.status == status)
        return self.session.exec(bet).all()

    def encontrar_apostas_status(self, game_id, status):
        bet = select(BetsModel).where(BetsModel.game_id == game_id, BetsModel.status == status)
        return self.session.exec(bet).all()

    def encontrar_apostas_user(self, user_id, status):
        bet = select(BetsModel).where(BetsModel.user_id == user_id, BetsModel.status == status)
        dados = self.session.exec(bet).all()
        return dados

    def encontar_apostas_id(self, user_id):
        bet = select(BetsModel).where(BetsModel.user_id == user_id)
        dados = self.session.exec(bet).all()
        return dados
    
    def atualizar_aposta_status(self, user_id, game_id, status, new_status):
        dados = self.buscar_aposta(user_id=user_id, game_id=game_id, status=status)
        for aposta in dados:
            aposta.status = new_status
            self.session.add(aposta)
        self.session.commit()

    def buscar_aposta_pendente(self, user_id, game_id):
        bet = select(BetsModel).where(BetsModel.user_id == user_id, BetsModel.game_id == game_id, BetsModel.status == "pendente")
        dados = self.session.exec(bet).first()
        return dados

    def atualizar_aposta_pontos(self, user_id, game_id, status, new_points):
        dados = self.buscar_aposta(user_id=user_id, game_id=game_id, status=status)
        for aposta in dados:
            aposta.points = new_points
            self.session.add(aposta)
        self.session.commit()

    def mostrar_pontos_apostado(self, user_id, game_id, status):
        dados = self.buscar_aposta(user_id=user_id, game_id=game_id, status=status)
        pontos = 0
        for aposta in dados:
            pontos = aposta.points
        return pontos

    def contagem_users_aposta(self, game_id: int, time_escolhido_id: int, status):
        dados = (select(func.count(func.distinct(BetsModel.user_id))).where(BetsModel.game_id == game_id, BetsModel.time_escolhido_id == time_escolhido_id, BetsModel.status == status))
        return self.session.exec(dados).one()

    def contagem_aposta(self):
        bet = (select(BetsModel.user_id, func.count(BetsModel.id).label("acertos")).where(BetsModel.status == "ganho").group_by(BetsModel.user_id).order_by(func.count(BetsModel.id).desc()))
        return self.session.exec(bet).all()
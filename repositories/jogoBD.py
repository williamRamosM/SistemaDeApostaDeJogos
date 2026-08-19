from sqlmodel import Session, SQLModel, select
from repositories.connectionBD import engine
from repositories.models.jogos import JogosModel
from sqlalchemy.exc import IntegrityError

class JogoBD:
    def __init__(self, session:Session):
        self.session = session

    def registrar_jogo(self, incremental_id, team_one, team_two, date_game, status, status_game):
        jogo = JogosModel(incremental_id=incremental_id, team_one=team_one, team_two=team_two, date_game=date_game, status=status, jogo_iniciado=status_game)
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)
        
    def buscar_existencia(self, id):
        informacao = select(JogosModel).where(JogosModel.incremental_id == id)
        return self.session.exec(informacao).first()
        
    def atualizar_jogo(self, incremental_id, date_game, status, jogo_iniciado, placar_one, placar_two):
        jogo = self.buscar_existencia(id=incremental_id)

        if date_game is not None:
            jogo.date_game = date_game
        if status is not None:
            jogo.status = status

        if jogo_iniciado is not None:
            jogo.jogo_iniciado = jogo_iniciado

        if placar_one is not None:
            jogo.placar_one = placar_one

        if placar_two is not None:
            jogo.placar_two = placar_two

        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)

    def atualizar_status(self, incremental_id):
        jogo = self.buscar_existencia(id=incremental_id)
        jogo.status = True
        self.session.add(jogo)
        self.session.commit()
        self.session.refresh(jogo)

    def mostrar_jogos_incremental(self, id):
        value = self.buscar_existencia(id=id)
        lista = [value.team_one, value.team_two]
        return lista

    def mostrar_pontos_partida(self, id):
        value = self.buscar_existencia(id=id)
        lista = [value.placar_one, value.placar_two]
        return lista
    
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

    def encontrar_id(self, incremental_id):
        dados = self.buscar_existencia(id=incremental_id)

        if dados is not None:
            return dados.id
        return None

    def buscar_jogos_times(self, id_time):
        informacao = select(JogosModel).where((JogosModel.team_one == id_time) | (JogosModel.team_two == id_time))
        dados = self.session.exec(informacao).all()
        lista = []
        for jogo in dados:
            if jogo.placar_one is not None:
                dicionario = {
                    "data": jogo.date_game,
                    "team_one": jogo.team_one,
                    "placar_one": jogo.placar_one,
                    "team_two": jogo.team_two,
                    "placar_two": jogo.placar_two,
                }
                lista.append(dicionario)
        return lista
    
    def buscar_jogos(self, status):
        dados = select(JogosModel).where(JogosModel.status == status)
        return self.session.exec(dados).all()
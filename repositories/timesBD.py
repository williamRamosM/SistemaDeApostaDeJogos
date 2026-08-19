from sqlmodel import Session, SQLModel, select
from sqlalchemy.exc import IntegrityError
from repositories.models.time import TimeModel

class TimesBD:
    def __init__(self, session:Session):
        self.session = session

    def cadastrar_time(self, incremental_id, name):
        time = TimeModel(incremental_id=incremental_id, name=name)
        self.session.add(time)
        self.session.commit()
        self.session.refresh(time)
        return time

    def buscar_existencia(self, id):
        informacao = select(TimeModel).where(TimeModel.incremental_id == id)
        return self.session.exec(informacao).first()

    def encontrar_nome_times(self, incremental_id):
        dados = self.buscar_existencia(id=incremental_id)
        if dados is None:
            return "desconhecido"
        return dados.name

    def capturar_infor_times(self):
        informacao = select(TimeModel)
        dados = self.session.exec(informacao).all()
        lista = []
        for time in dados:
            dicionario = {
                "id_incremental": time.incremental_id,
                "nome": time.name
            }
            lista.append(dicionario)
        return lista

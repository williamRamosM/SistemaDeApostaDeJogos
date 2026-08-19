from sqlmodel import Session
from api_services.api_generico import ApiGenerico
from repositories.timesBD import TimesBD
from repositories.connectionBD import engine

class Time:
    def sicronizar_dados_times(self):
        api = ApiGenerico()
        informacoes = api.encontrar_informacao(tipo="matches")

        with Session(engine) as session:
            banco = TimesBD(session=session)
            for dados in informacoes.get("matches", []):
                for time in (dados["homeTeam"], dados["awayTeam"]):
                    id = time["id"]
                    existe = banco.buscar_existencia(id = id)
                    if existe:
                        continue
                    banco.cadastrar_time(
                        incremental_id=id,
                        name=time["name"]
                    )
    
    def nome_time_id(self, id_time):
        with Session(engine) as session:
            banco = TimesBD(session=session)
            nome = banco.encontrar_nome_times(incremental_id=id_time)
        return nome

    def mostrar_times(self):
        with Session(engine) as session:
            banco = TimesBD(session=session)
            lista = banco.capturar_infor_times()
        return lista
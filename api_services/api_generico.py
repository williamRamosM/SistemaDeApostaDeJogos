import requests
from config import TOKEN, API_URL
class ApiGenerico:

    def encontrar_informacao(self, tipo):
        headers = {'X-Auth-Token': TOKEN}
        url_tipo = f"{API_URL}{tipo}"
        resposta = requests.get(url=url_tipo,headers=headers, timeout=10)

        if(resposta.status_code == 200):
            produto = resposta.json()
        else:
            raise ValueError("System > Falha ao se comunicar com a api!")
        return produto
        
import requests
from config import TOKEN, API_URL
class ApiGenerico:

    def encontrar_informacao(self, tipo):
        resposta = requests.get(url=API_URL,headers=TOKEN)

        if(resposta.status_code == 200):
            produto = resposta.json().get(tipo)
            print(produto)
        else:
            raise ValueError("System > Falha ao se comunicar com a api!")
        
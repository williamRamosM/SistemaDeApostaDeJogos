from services.jogos import Jogos
from services.usuario import Usuario
from compilar import Compilar

compilar = Compilar()
game = Jogos()

compilar.criar_aposta_admin()

#game.sicronizar_dados_jogos()
#game.atualizar_dodos()
#print(game.mostrar_jogo_usuario())


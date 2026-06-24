from argon2 import PasswordHasher
from dotenv import load_dotenv
import hmac
import hashlib
import os

class SecurityPassWorld:

    load_dotenv(dotenv_path=".env")

    def __init__(self):
        self.pepper = os.getenv("PEPPER_SECRET").encode() #Lendo a informacao e transcrevendo para bytes.
        self.hasher = PasswordHasher(time_cost=2,memory_cost=65536,parallelism=2) #criar valores para deixar mais dificil a senha.

    def _aplicar_pepper(self, passworld):
        return hmac.new(self.pepper, passworld.encode(), hashlib.sha256).hexdigest()
    
    def codificar_senha(self, passworld):
        return self.hasher.hash(self._aplicar_pepper(passworld=passworld))

    def autenticar_senha(self, passworld_atual, password_salvo):
        return self.hasher.verify(password_salvo, self._aplicar_pepper(passworld=passworld_atual))


import bcrypt 
import os

class SecurityPassWorld:

    PEPPER = os.getenv("PEPPER_SECRET")
    PEPPER_SECRET = PEPPER.encode("")

    def rescrever_senha(passworld):
       a=1
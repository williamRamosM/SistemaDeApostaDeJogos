import unicodedata
class Security_Username:

    def __init__(self):
        
          with open(r"names.txt", "r", encoding="utf-8") as arquivo:
            self.invalid_names = set(arquivo.read().splitlines())
            self.dicionary = {
                "0":"o",  "1":"i",  "3":"e",
                "4":"a",  "7": "t", "8": "b",
                "9": "g", "@": "a", "$": "s",
                "!": "i", "*": "u"
            }

    def rescrever_username(self, username:str):
        name = username.lower()
        name = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode("utf-8")
        new_username = name
        for key, valuer in self.dicionary.items():
            new_username = new_username.replace(key, valuer)
        return new_username
    
    def verificar_username(self, username:str):
        new_username = self.rescrever_username(username)
        for value in self.invalid_names:
            if(new_username in value):
                return False
        return True
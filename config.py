from dotenv import load_dotenv
import os

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")
PEPPER = os.getenv("PEPPER_SECRET")
TOKEN = {'X-Auth-Token': '554b4d533d1d4655a8ea33dc9e09b907'}
API_URL = "https://api.football-data.org/v4/"
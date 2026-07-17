from dotenv import load_dotenv
import os

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")
PEPPER = os.getenv("PEPPER_SECRET")
TOKEN = os.getenv("TOKEN")
API_URL = os.getenv("API_URL")
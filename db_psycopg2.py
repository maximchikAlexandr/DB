import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

password_db  = os.getenv('password_db')

conn = psycopg2.connect(database="postgres", user="postgres", password=password_db)
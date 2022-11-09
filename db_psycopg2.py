import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

password_db  = os.getenv('password_db')

conn = psycopg2.connect(database="postgres", user="postgres", password=password_db)

cur = conn.cursor()

cur.execute('SELECT 1')
data = cur.fetchone()
print(data, type(data))

cur.close()
conn.close()

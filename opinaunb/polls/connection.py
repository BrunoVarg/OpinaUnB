import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

class Connection:

    def __init__(self):
        self.conn = psycopg2.connect(
                    host = os.getenv("HOST_DB"),
                    database = os.getenv("DATABASE_DB"),
                    user = os.getenv("USER_DB"),
                    password = os.getenv("PASSWORD_DB")
                    )
        
    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        aux = cur.fetchone()
        print(aux)
        if aux:
            val = aux[0]
            cur.close()
            return val
        cur.close()
        return None
    
    def get_one(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        aux = cur.fetchone()
        cur.close()
        return aux

    def get_all(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        aux = cur.fetchall()
        cur.close()
        return aux
    
    def get(self, query):
        cur = self.conn.cursor()
        val = cur.execute(query)
        cur.close()
        return val
    
    def update(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()
        return

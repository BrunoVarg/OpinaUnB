import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

from opinaunb.polls.connection import Connection
from opinaunb.polls.cruds.usuario import create_user, get_matricula

con = Connection()
create_user(con, 123456, True, "Bruno Vargas", "brunovargas@email", "CIC", "senha")
create_user(con, 11111, False, "usuario", "usuario@email", "CIC", "1234")
create_user(con, 00000, False, "usuario2", "usuario2@email", "CIC", "1234")

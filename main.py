import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

from opinaunb.polls.connection import Connection
from opinaunb.polls.cruds.usuario import create_user, get_matricula
from opinaunb.polls.cruds.avaliacao_professor import create_avaliacao_professor, get_nota, call_procedure_avaliacoes
from opinaunb.polls.cruds.all import get_last_value

con = Connection()
#create_user(con, 123456, True, "Bruno Vargas", "brunovargas@email", "CIC", "senha")
#create_user(con, 11111, False, "usuario", "usuario@email", "CIC", "1234")
#create_user(con, 00000, False, "usuario2", "usuario2@email", "CIC", "1234")

call_procedure_avaliacoes(con, "Algum comentário", 123456, 32877, 1, 7)
call_procedure_avaliacoes(con, "Algum comentário", 11111, 32877, 1, 9)



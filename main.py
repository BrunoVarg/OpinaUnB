import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

from opinaunb.polls.connection import Connection
from opinaunb.polls.cruds.usuario import create_user, get_matricula
from opinaunb.polls.cruds.avaliacao_professor import create_avaliacao_professor, get_nota, call_procedure_avaliacoes
from opinaunb.polls.cruds.all import get_last_value
from opinaunb.polls.cruds.denuncias import create_denuncia

con = Connection()
create_user(con, 123456, True, "Bruno Vargas", "brunovargas@email", "CIC", "senha")
create_user(con, 11111, False, "usuario", "usuario@email", "CIC", "senha")
create_user(con, 22222, False, "usuario2", "usuario2@email", "MAT", "senha")
create_user(con, 33333, False, "usuario3", "usuario3@email", "EST", "senha")

# Cria comentario para Turma e Professor
call_procedure_avaliacoes(con, "Gostei!", 123456, 32877, 1, 7)
call_procedure_avaliacoes(con, "Adorei, muito bom!!!", 11111, 32877, 1, 9)
call_procedure_avaliacoes(con, "Simplesmente Sensacional! Nota 10!", 22222, 32877, 1, 10)

call_procedure_avaliacoes(con, "@#&$%*&!", 123456, 32877, 1, 7)
call_procedure_avaliacoes(con, "$%$##%@!@#!@#%*$&@#&!!!", 11111, 32877, 1, 9)
call_procedure_avaliacoes(con, "!&$@*(@#!@!)", 22222, 32877, 1, 10)

# Denuncia as 3 primeiras avaliacoes
create_denuncia(con, 4)
create_denuncia(con, 5)
create_denuncia(con, 6)



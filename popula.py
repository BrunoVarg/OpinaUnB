from opinaunb.polls.connection import Connection
import os
import pandas as pd
import time
import math
from .opinaunb.polls.cruds.usuario import create_user

con = Connection()

count_prof = 1
dict_prof = {}

path_turmas, path_depto, path_disciplinas = [[], [], []]
for root, dirs, files in os.walk("./data", topdown=False):
    for name in files:
        path = os.path.join(root, name)
        if 'turmas' in path:
            path_turmas.append(path)
        elif 'departamento' in path:
            path_depto.append(path)
        else:
            path_disciplinas.append(path)
            

# Popula Departamento

for path in path_depto:
    data = pd.read_csv(path)

    for cod, nome in zip(data.cod, data.nome):
        if not con.query(f"SELECT EXISTS(SELECT * FROM Departamentos WHERE nome='{nome}')"):
            con.update(f"INSERT INTO Departamentos (codigo, nome) VALUES({cod}, '{nome}')")

for path in path_disciplinas:
    data = pd.read_csv(path)

    for cod, nome, cod_dep in zip(data.cod, data.nome, data.cod_depto):
        if not con.query(f"SELECT EXISTS(SELECT * FROM Disciplinas WHERE codigo='{cod}')"):
            con.update(f"INSERT INTO Disciplinas (codigo, nome, fk_cod_dep) VALUES('{cod}', '{nome}', {cod_dep})")
        
    

# Popula Professor

for path in path_turmas:
    data = pd.read_csv(path)
    for prof, dpto in zip(data.professor, data.cod_depto):
        prof = prof[:-6]

        if not con.query(f"SELECT EXISTS(SELECT * FROM Professores WHERE nome='{prof}')"):
            val = con.query(f"SELECT COUNT(id) FROM Professores")
            con.update(f"INSERT INTO Professores (id, nome, fk_cod_dep) VALUES({val+1}, '{prof}', {dpto})")

# Popula Turmas

for path in path_turmas:
    data = pd.read_csv(path)
    for turma,periodo,professor,horario,vagas_ocupadas,total_vagas,local,cod_disciplina,cod_depto in \
        zip(data.turma, data.periodo, data.professor, data.horario, data.vagas_ocupadas, data.total_vagas, data.local, data.cod_disciplina, data.cod_depto):
        prof = professor[:-6]
        fk_prof = con.query(f"SELECT * FROM Professores WHERE nome='{prof}'")

        if math.isnan(total_vagas):
            total_vagas = 0
        if math.isnan(vagas_ocupadas):
            vagas_ocupadas = 0

        #print(type(total_vagas), vagas_ocupadas)
        # turma, periodo, professor cod_disciplina, cod_depto
        if not con.query(f"SELECT EXISTS(SELECT * FROM Turmas WHERE turma='{turma}' AND periodo='{periodo}' AND fk_professor={fk_prof} AND fk_cod_disciplina='{cod_disciplina}' AND fk_cod_dep={cod_depto})"):
            val = con.query(f"SELECT COUNT(id) FROM Turmas")
            con.update(f"INSERT INTO Turmas (id, turma, periodo, horario, vagas_ocupadas, total_vagas, local, fk_professor, fk_cod_disciplina, fk_cod_dep) VALUES\
                       ({val+1}, '{turma}', '{periodo}', '{horario}', {vagas_ocupadas}, {total_vagas}, '{local}', {fk_prof},'{cod_disciplina}', {cod_depto})")


create_user(con, 123456, True, "Bruno Vargas", "brunovargas@email", "CIC", "senha")

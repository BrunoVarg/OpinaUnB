
from ..connection import Connection
con = Connection()
def get_all_departamentos(conn):
    return conn.get_all("SELECT * FROM Departamentos")

def get_all_disciplinas(conn):
    return conn.get_all("SELECT * FROM Disciplinas")

def get_all_professores(conn):
    return conn.get_all("SELECT * FROM Professores")

def get_disciplinas_departamento(conn, codigo):
    return conn.get_all(f"SELECT * FROM Disciplinas where fk_cod_dep={codigo}")

def get_name_by_cod_dep(codigo, conn = con):
    return conn.get_one(f"SELECT nome FROM Departamentos where codigo={codigo}")

def get_prof_by_codigo(codigo, conn = con):
    return conn.get_all(f"SELECT * FROM Professores where id={codigo}")

def get_one_prof_by_codigo(codigo, conn = con):
    return conn.get_one(f"SELECT * FROM Professores where id={codigo}")

def get_prof_filtered(codigo, disciplina, conn = con):
    if codigo != 'None' and disciplina != 'None':
        return conn.get_all(f"SELECT fk_professor FROM Turmas where fk_cod_disciplina='{disciplina}' AND fk_cod_dep={int(codigo)}")
    elif codigo != 'None':
        return conn.get_all(f"SELECT fk_professor FROM Turmas where fk_cod_dep={int(codigo)}")


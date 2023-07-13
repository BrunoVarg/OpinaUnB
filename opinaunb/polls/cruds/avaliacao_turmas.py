from ..connection import Connection
from datetime import date
from .all import get_last_value

def get_id_avaliacao(conn: Connection, id):
    return conn.query(f"SELECT * FROM Avaliacoes WHERE is_turma=true AND id={id}")

def get_professor_by_dep_disciplina(conn:Connection, dep, disciplina):
    return conn.get_all(f"SELECT * FROM Turmas WHERE fk_cod_dep={dep} AND fk_cod_disciplina='{disciplina}';")

def get_professor_by_dep(conn:Connection, dep):
    return conn.get_all(f"SELECT * FROM Turmas WHERE fk_cod_dep={dep};")

def get_professor_by_disciplina(conn:Connection, disciplina):
    return conn.get_all(f"SELECT * FROM Turmas WHERE fk_cod_disciplina='{disciplina}';")

def get_all_turmas(conn: Connection):
    return conn.get_all(f"SELECT * FROM Turmas")

def get_name_by_cod_disciplina(conn:Connection, codigo):
    return conn.get_one(f"SELECT nome FROM Disciplinas where codigo='{codigo}'")

def get_all_turmas_prof_disc(conn: Connection, prof, disciplina):
    return conn.get_all(f"SELECT * FROM Turmas WHERE fk_professor={prof} AND fk_cod_disciplina='{disciplina}';")

def get_all_avaliacoes(conn:Connection, turma):
    return conn.get_all(f"SELECT * FROM Avaliacoes WHERE is_turma=true AND fk_turma={turma};")

def get_periodos(conn:Connection, disciplina, professor):
    return conn.get_all(f"SELECT periodo FROM Turmas WHERE fk_professor={professor} AND fk_cod_disciplina='{disciplina}';")

def get_num_turma(conn:Connection, disciplina, professor, periodo):
    return conn.get_all(f"SELECT turma FROM Turmas WHERE fk_professor={professor} AND fk_cod_disciplina='{disciplina}' AND periodo='{periodo}';")

def get_id_turma(conn:Connection, disciplina, professor, periodo, turma):
    return conn.get_one(f"SELECT id FROM Turmas WHERE fk_professor={professor} AND fk_cod_disciplina='{disciplina}' AND periodo='{periodo}' AND turma='{turma}';")

def create_avaliacao_turmas(conn: Connection, comentario, turma, matricula, nota):
    val = get_last_value('Avaliacoes')
    conn.update(f"INSERT INTO Avaliacoes (id, comentario, is_turma, fk_turma, fk_matricula, nota, data) VALUES({val}, '{comentario}', {True}, '{turma}', {matricula}, {nota}, '{date.today()}')")
    return "Avaliação Cadastrada."

def get_avaliacoes_turmas(conn, pk):
    return conn.get_one(f"SELECT * FROM Avaliacoes WHERE id={pk};")

def update_avaliacao_turma(conn: Connection, id, comentario, matricula, turma, nota):
    conn.update(f"UPDATE Avaliacoes set comentario='{comentario}', is_turma={True}, fk_matricula={matricula}, fk_turma='{turma}', nota={nota}, data='{date.today()}' WHERE id={id}")

def delete_avaliacao_turma(conn: Connection, id):
    if get_id_avaliacao(conn, id):
        conn.update(f"DELETE FROM Avaliacoes WHERE id = {id}")


def get_nota_turma(conn, professor, disciplina):
    all_turmas = []
    return conn.query(f"SELECT AVG(nota) FROM Notas_professor WHERE fk_professor={id}")

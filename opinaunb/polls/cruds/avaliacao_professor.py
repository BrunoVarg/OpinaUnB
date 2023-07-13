from ..connection import Connection
from datetime import date

from .all import get_last_value

def get_all_avaliacoes_professores(conn: Connection, codigo):
    return conn.get_all(f"SELECT * FROM Avaliacoes WHERE is_turma=false AND fk_professor={codigo};")

def get_avaliacoes_professores(conn, pk):
    return conn.get_one(f"SELECT * FROM Avaliacoes WHERE id={pk};")

def get_id_avaliacao(conn: Connection, id):
    return conn.query(f"SELECT * FROM Avaliacoes WHERE is_turma=false AND id={id}")

def create_avaliacao_professor(conn: Connection, comentario, matricula, professor, nota):
    val = get_last_value('Avaliacoes')
    conn.update(f"INSERT INTO Avaliacoes (id, comentario, is_turma, fk_matricula, fk_professor, nota, data) VALUES({val+1}, '{comentario}', {False}, {matricula}, '{professor}', {nota}, '{date.today()}')")
    return "Avaliação Cadastrada."

def delete_avaliacao(conn: Connection, id):
    if get_id_avaliacao(conn, id):
        conn.update(f"DELETE FROM Avaliacoes WHERE id = {id}")

def update_avaliacao(conn: Connection, id, comentario, matricula, professor, nota):
    conn.update(f"UPDATE Avaliacoes set comentario='{comentario}', is_turma={False}, fk_matricula={matricula}, fk_professor={professor}, nota={nota}, data='{date.today()}' WHERE id={id}")

def get_nota(conn, id):
    return conn.query(f"SELECT AVG(nota) FROM Notas_professor WHERE fk_professor={id}")

"""
    Procedure que insere 2 tipos de valores diferentes nas tabelas, is_truma = true e is_truma = false
"""
def call_procedure_avaliacoes(conn, comentario, matricula, turma, professor, nota):
    conn.update(f"CALL inserir_avaliacoes({get_last_value('avaliacoes')}, '{comentario}', {matricula}, {turma}, {professor}, {nota}, '{date.today()}')")

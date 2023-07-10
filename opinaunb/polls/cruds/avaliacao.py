
def get_all_avaliacoes(conn):
    return conn.query("SELECT * FROM Avaliacoes")

def get_id_avaliacao(conn, id):
    return conn.query(f"SELECT * FROM Avaliacoes WHERE id={id}")

def create_avaliacao(conn, comentario, is_turma, matricula, turma, professor, nota):
    val = conn.query(f"SELECT COUNT(id) FROM Avaliacoes")
    conn.query(f"INSERT INTO Avaliacoes (id, comentario, is_turma, fk_matricula, fk_turma, fk_professor, nota) VALUES({val+1}, '{comentario}', {is_turma}, {matricula}, {turma}, '{professor}', {nota})")
    return "Avaliação Cadastrada."

def delete_avaliacao(conn, id):
    if get_id_avaliacao(id):
        conn.query(f"DELETE FROM Avaliacoes WHERE id = {id}")

def update_avaliacao(conn, id, comentario, is_turma, matricula, turma, professor, nota):
    conn.update(f"UPDATE Avaliacoes set comentario='{comentario}', is_turma={is_turma}, matricula={matricula}, turma={turma}, professor={professor}, nota={nota} WHERE id={id}")

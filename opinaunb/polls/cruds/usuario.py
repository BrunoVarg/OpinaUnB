
class User:
    def __init__(self, matricula, is_adm, nome, email, curso, senha):
        self.matricula = matricula
        self.is_adm = is_adm
        self.nome = nome
        self.email = email
        self.curso = curso
        self.senha = senha


def get_all_users(conn):
    return conn.get_all("SELECT * FROM Estudantes")

def get_matricula(conn, matricula):
    return conn.get_one(f"SELECT * FROM Estudantes WHERE matricula={matricula}")

def get_email(conn, email):
    return conn.query(f"SELECT * FROM Estudantes WHERE email='{email}'")

def check_login(conn, matricula, senha):
    return bool(conn.query(f"SELECT EXISTS(SELECT * FROM Estudantes WHERE matricula={matricula} AND senha='{senha}')"))

def create_user(conn, matricula, is_adm, nome, email, curso, senha):
    if(get_matricula(conn, matricula)):
        return "Matricula já cadastrada."
    
    if(get_email(conn, email)):
        return "E-mail já cadastrado."
    
    conn.update(f"INSERT INTO Estudantes (matricula, is_adm, nome, email, curso, senha) VALUES({matricula}, {is_adm}, '{nome}', '{email}', '{curso}', '{senha}')")
    return "Estudante Cadastrado."

def delete_user(conn, matricula):
    if get_matricula(matricula):
        conn.query(f"DELETE FROM Estudantes WHERE matricula = {matricula}")

def update_user(conn, matricula, is_adm, nome, email, curso, senha):
    conn.update(f"UPDATE Estudantes set is_adm={is_adm}, nome='{nome}', email='{email}', curso='{curso}', senha='{senha} WHERE matricula={matricula}'")

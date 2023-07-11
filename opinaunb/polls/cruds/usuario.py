import psycopg2
import os
from base64 import b64encode

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Navegar duas pastas anteriores
diretorio_pai = os.path.dirname(diretorio_atual)
diretorio_avo = os.path.dirname(diretorio_pai)
caminho_profile = os.path.join(diretorio_avo, 'static', 'image', 'profile.png')

with open(caminho_profile, 'rb') as f:
    imagem_profile = f.read()

class User:
    def __init__(self, matricula, is_adm, nome, email, curso, senha, imagem):
        self.matricula = matricula
        self.is_adm = is_adm
        self.nome = nome
        self.email = email
        self.curso = curso
        self.senha = senha
        self.imagem = imagem


def get_all_users(conn):
    return conn.get_all("SELECT * FROM Estudantes")

def get_matricula(conn, matricula):
    return conn.get_one(f"SELECT * FROM Estudantes WHERE matricula={matricula}")

def get_email(conn, email):
    return conn.query(f"SELECT * FROM Estudantes WHERE email='{email}'")

def get_image(conn, matricula):
    return b64encode(conn.get_one(f"SELECT imagem FROM Estudantes WHERE matricula = {matricula}")[0]).decode('utf-8')

def check_login(conn, matricula, senha):
    return bool(conn.query(f"SELECT EXISTS(SELECT * FROM Estudantes WHERE matricula={matricula} AND senha='{senha}')"))

def create_user(conn, matricula, is_adm, nome, email, curso, senha, imagem=imagem_profile):
    if(get_matricula(conn, matricula)):
        return "Matricula já cadastrada."
    
    if(get_email(conn, email)):
        return "E-mail já cadastrado."
    
    conn.update(f"INSERT INTO Estudantes (matricula, is_adm, nome, email, curso, senha, imagem) VALUES({matricula}, {is_adm}, '{nome}', '{email}', '{curso}', '{senha}', {psycopg2.Binary(imagem)})")
    return "Estudante Cadastrado."

def edit_user(conn, matricula, is_adm, nome, email, curso, senha, imagem):
    print(matricula, nome, email, curso, senha, imagem)
    if nome:
        conn.update(f"UPDATE Estudantes SET nome='{nome}' WHERE matricula = {matricula}")
    
    if email:
        if not get_email(conn, email):
            conn.update(f"UPDATE Estudantes SET email='{email}' WHERE matricula = {matricula}")
    
    if curso:
        print("CURSO")
        conn.update(f"UPDATE Estudantes SET curso='{curso}' WHERE matricula = {matricula}")
    
    if senha:
        conn.update(f"UPDATE Estudantes SET senha='{senha}' WHERE matricula = {matricula}")
    
    if imagem:
        conn.update(f"UPDATE Estudantes SET imagem={psycopg2.Binary(imagem)} WHERE matricula = {matricula}")

def delete_user(conn, matricula):
    if get_matricula(conn, matricula):
        conn.update(f"DELETE FROM Estudantes WHERE matricula = {matricula}")

def update_user(conn, matricula, is_adm, nome, email, curso, senha):
    conn.update(f"UPDATE Estudantes set is_adm={is_adm}, nome='{nome}', email='{email}', curso='{curso}', senha='{senha} WHERE matricula={matricula}'")

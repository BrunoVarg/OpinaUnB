from ..connection import Connection
from datetime import date
from .all import get_last_value


def get_all_denuncias(conn: Connection):
    return conn.get_all(f"SELECT * FROM Denuncias;")

def get_denuncia_avaliacao(conn: Connection, id):
    return conn.get_one(f"SELECT * FROM Avaliacoes WHERE id={id};")

def create_denuncia(conn: Connection, id):
    val = get_last_value('Denuncias')
    conn.update(f"INSERT INTO Denuncias (id, fk_id_avaliacao) VALUES({val}, {id})")

def call_denuncia(conn, option, denuncia, avaliacao, matricula):
    conn.update(f"CALL AcaoDenuncia({option}, {denuncia}, {avaliacao}, {matricula})")

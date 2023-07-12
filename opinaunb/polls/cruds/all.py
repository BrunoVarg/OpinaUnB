from ..connection import Connection
con = Connection()

def get_last_value(name_table, conn = con):
    return conn.query(f"SELECT COALESCE(MAX(id), 0) + 1 AS proximo_id_vazio FROM {name_table};")
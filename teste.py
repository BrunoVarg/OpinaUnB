from opinaunb.polls.cruds.filter import get_all_departamentos, get_all_disciplinas, get_all_professores

from opinaunb.polls.connection import Connection
con = Connection()
lista = [(x, y) for x,y in get_all_departamentos(con)]
lista2 = [(x[0], x[1]) for x in get_all_disciplinas(con)]

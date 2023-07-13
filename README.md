# Trabalho Prático Banco de Dados

- Projeto implementado usando [PostgreSQL](https://www.postgresql.org/download/) em linux.

## Instalando Dependencias

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

```bash
pip install -r requirements.txt
```

## Configurando o Banco de Dados

```bash
psql -U nome_usuario -d nome_banco_de_dados
```

```bash
\i /sql/create.sql
```

- Altere no arquivo .env as variaveis DATABASE_DB, USER_DB, PASSWORD_DB, de acordo com o que foi criado anteriormente


## Rodando a Aplicação

- Populando o banco

```bash
python3 main.py
```

```bash
cd opinaunb
```

```bash
python3 manage.py runserver
```

- Acesse a url http://localhost:8000/polls/
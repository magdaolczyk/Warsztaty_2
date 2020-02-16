from psycopg2 import connect


def connect_local(db="warsztaty_db"):
    cnx = connect(user="postgres", password="coderslab",
                host="localhost", database=db)
    cnx.autocommit = True
    return cnx

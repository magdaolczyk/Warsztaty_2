from psycopg2 import connect


def connect_local(db="warsztaty_db"):
    cnx = connect(user="postgres", password="coderslab",
                host="localhost", database=db)
    cnx.autocommit = True
    return cnx



#Tworzenie backupu
# pg_dump -U [user_name] -W -h [host] database > [file].sql
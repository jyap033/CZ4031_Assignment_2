import psycopg2


def connect():
    # Configurations
    connection_string = "dbname=cz4031 user=postgres password='admin'"
    database_name = 'cz4031'
    conn = None

    print('Connecting to the PostgreSQL database...')

    conn = psycopg2.connect(connection_string)
    print('Connected')

    cur = conn.cursor()

    cur.execute("SELECT datname FROM pg_database;")
    list_database = cur.fetchall()

    if (database_name,) not in list_database:
        sqlCreateDatabase = "create database " + database_name + ";"
        cur.execute(sqlCreateDatabase)

    else:
        print("{} database already exist.".format(database_name))
    cur.execute(
        "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")

    list_tables = list(map(lambda x: x[0], cur.fetchall()))

    table_dict = {}

    for i in list_tables:
        cur.execute("SELECT column_name FROM information_schema.columns WHERE TABLE_NAME = '{}';".format(i))
        column = list(map(lambda x: x[0], cur.fetchall()))
        table_dict[i] = column
    return conn, table_dict

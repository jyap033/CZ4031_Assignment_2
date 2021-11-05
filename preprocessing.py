from typing import Dict
import psycopg2

def read_config(filename: str) -> Dict:
    configs = {}
    with open(filename) as config_file:
        for line in config_file:
            key, value = line.split("=")
            configs[key] = value.rstrip("\n")
    print(f"configs: {configs}")
    return configs


def connect():
    # Configurations
    configs = read_config("CONFIG.txt")
    database_name = configs["DBNAME"]
    connection_string = f"dbname={database_name} user={configs['USER']} password={configs['PASSWORD']}"
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

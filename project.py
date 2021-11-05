
import psycopg2
from preprocessing import connect
from interface import *

if __name__ == "__main__":
    conn = None
    try:
        startup = connect()
        conn = startup[0]
        tables = startup[1]
        gui = interface(conn, tables)
        gui.initialise()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

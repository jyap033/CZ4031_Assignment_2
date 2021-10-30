
#MAIN running
import psycopg2

from preprocessing import connect
from interface import *

if __name__ == "__main__":
    conn = None
    try:
        conn = connect()
        gui = interface(conn)
        gui.gui()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

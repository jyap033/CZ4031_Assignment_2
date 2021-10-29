
#MAIN running
import psycopg2

from preprocessing import connect
from interface import *

if __name__ == "__main__":
    try:
        connect()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        gui = interface()
        gui.gui()


import psycopg2


def connect():
    """ Connect to the PostgreSQL database server """

    #Configurations
    connection_string = "dbname=myfirstdb user=postgres password='admin'"
    database_name = 'myfirstdb'
    conn = None
    try:
        # read connection parameters
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')

        ##
        conn = psycopg2.connect(connection_string)
        print('Connected')

        # create a cursor
        cur = conn.cursor()

        #Execute Query
        cur.execute("SELECT datname FROM pg_database;")

        #Get Query Result
        list_database = cur.fetchall()

       # cur.execute("EXPLAIN SELECT * FROM \"Movies\"")
        cur.execute("EXPLAIN ANALYSE Select * From \"Movies\" m, \"Ratings\" r Where m.\"Name\" = R.\"Name\"")
        print(cur.fetchall())



        if (database_name,) not in list_database:
            sqlCreateDatabase = "create database " + database_name + ";"
            cur.execute(sqlCreateDatabase)
            # print("'{}' has been created successfully.".format(database_name))
        #to be deleted
        else:
            print("{} database already exist.".format(database_name))
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



import psycopg2

connection = None
try:
    print("Attempting to connect to the database...")
    connection = psycopg2.connect(
        database="mydatabase",
        user="postgres",
        password="mypassword",
        host="localhost",
        port="5433"
    )
    print("Connection to the database was successful.")

    # cursor = connection.cursor()
    # print("Executing a test query...")
    # cursor.execute("SELECT version();")
    # record = cursor.fetchone()
    # print("You are connected to - ", record, "\n")
except psycopg2.OperationalError as e:
    print("OperationalError:", e)
except psycopg2.Error as e:
    print("Error:", e)
finally:
    if connection is not None:
        # cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")



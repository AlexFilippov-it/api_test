import psycopg2


def get_db_connection():
    conn = psycopg2.connect(database="sarova", user="postgres", password="postgres",
                            host="localhost", port="5432")
    return conn

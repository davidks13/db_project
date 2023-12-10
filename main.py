import psycopg2

def database_exists(cursor, database_name):
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database_name,))
    return cursor.fetchone() is not None

def create_database(database_name, user, password, host, port):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
        )
        connection.autocommit = True

        cursor = connection.cursor()

        if not database_exists(cursor, database_name):
            cursor.execute(f"CREATE DATABASE {database_name}")
            print(f"Database '{database_name}' created successfully.")
        else:
            print(f"Database '{database_name}' already exists. Skipping creation.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    database_name = "sales_department"
    user = "####"
    password = "####"
    host = "####"
    port = "####"

    create_database(database_name, user, password, host, port)

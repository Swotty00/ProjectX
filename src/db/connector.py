import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

def apply_schema(conn, cursor):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(current_dir, "schema.sql")
    with open(schema_path, "r") as f:
        ddl = f.read()
        cursor.execute(ddl)
    
    conn.commit()

load_dotenv()

try:
    # Conectar com o DB com base nos parâmetros do .env
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

    cursor = conn.cursor()
    print("Conexão bem-sucedida ao PostgreSQL!")
    
    apply_schema(conn, cursor)

except Error as e:
    print(f"Erro ao conectar ou executar a query no PostgreSQL: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Conexão com PostgreSQL encerrada.")
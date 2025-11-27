import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os
import pandas as pd
from psycopg2.extras import execute_batch

def apply_schema(conn):
    cursor = conn.cursor()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(current_dir, "schema.sql")
    with open(schema_path, "r") as f:
        ddl = f.read()
        cursor.execute(ddl)
    
    conn.commit()
    cursor.close()

def insert_data_in_DB(pasteName, archive, conn):
    cursor = conn.cursor()
    current_dir = os.path.join(pasteName, archive)

    df = pd.read_csv(current_dir)
    df = df.rename(columns={'review': 'texto', 'sentiment': 'label'})
    data_to_insert = [tuple(row) for row in df[['texto', 'label']].values]
    
    insert_query = "INSERT INTO reviews (texto, label) VALUES (%s, %s)"
    execute_batch(cursor, insert_query, data_to_insert)

    conn.commit()
    print(f"Inserção de {len(data_to_insert)} registros concluída via execute_batch.")
    cursor.close()

def table_exists(conn, table_name):
    try:
        cursor = conn.cursor()

        query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
        );
        """

        cursor.execute(query, (table_name,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return exists
    except psycopg2.Error as e:
        print(f"Erro ao verificar a existência da tabela: {e}")
        return False

def connect_db():
    try:
        # Conectar com o DB com base nos parâmetros do .env
        conn = psycopg2.connect(
            host = os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )

        print("Conexão bem-sucedida ao PostgreSQL!")
        return conn

    except Error as e:
        print(f"Erro ao conectar ou executar a query no PostgreSQL: {e}")

def disconnect_db(conn):
    if conn:
        conn.close()
        print("Conexão com PostgreSQL encerrada.")
        

if __name__ == "__main__":
    load_dotenv()
    conn = connect_db()

    if not table_exists(conn, 'reviews'):
        print("Tabela 'reviews' não foi encontrada. Criando schema e populando banco...")
        apply_schema(conn)
        insert_data_in_DB("data", "IMDB Dataset.csv", conn)

    disconnect_db(conn)
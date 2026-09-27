import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():

    connection = psycopg2.connect(
        host="localhost",
        database="ai_knowledge_db",
        user="postgres",
        password="root",
        port="5432"
    )

    return connection


def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    # Chat messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100),
            role VARCHAR(20),
            message TEXT
        )
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    connection.commit()

    cursor.close()

    connection.close()

    print("Tables created successfully!")


if __name__ == "__main__":

    connection = get_connection()

    print("PostgreSQL connected successfully!")

    connection.close()

    create_table()
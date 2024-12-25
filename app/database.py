import psycopg2

DB_NAME = "scraping_demo"
DB_USER = "postgres"
DB_PASSWORD = "scrapingdemo"
DB_HOST = "localhost"
DB_PORT = "5433"

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

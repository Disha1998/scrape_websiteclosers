from app.database import get_db_connection
from scraper.scrape_details import scrape_details

def main():
    # Get the database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Call the detail page scraping function
        scrape_details(cursor, conn)
    finally:
        # Close the connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

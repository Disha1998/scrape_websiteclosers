from app.database import get_db_connection
from scraper.scrape_websiteclosers import scrape_website

def main():
    # Get the database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Call the scraping function
        scrape_website(cursor, conn)
    finally:
        # Close the connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

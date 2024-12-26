from app.database import get_db_connection
from scraper.scrape_websiteclosers import scrape_website
from scraper.scrape_details import scrape_details

def main():
    # Get the database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First, scrape the homepage listings
        print("Starting homepage scraping...")
        scrape_website(cursor, conn)
        print("Homepage scraping completed.")

        # Then, scrape the detail pages
        print("Starting detail page scraping...")
        scrape_details(cursor, conn)
        print("Detail page scraping completed.")
    finally:
        # Close the connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

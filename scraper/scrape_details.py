import requests
from bs4 import BeautifulSoup
from app.database import get_db_connection

def scrape_details(cursor, conn):
    # Fetch all URLs from the websiteclosers_listing table
    cursor.execute("SELECT id, url FROM websiteclosers_listing")
    listings = cursor.fetchall()  # List of tuples: (id, url)

    for listing_id, url in listings:
        print(f"Scraping details for Listing ID: {listing_id}, URL: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, skipping...")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract detailed description from the detail page (<p> tags inside a specific div)
        description_container = soup.find("div", class_="wysiwyg cfx")
        if description_container:
            description_tags = description_container.find_all("p")
            description = "\n".join(tag.get_text(strip=True) for tag in description_tags if tag.get_text(strip=True))
        else:
            description = None

        # Extract other details from the detail page
        gross_income_tag = soup.find("div", string="Gross Income").find_next("div") if soup.find("div", string="Gross Income") else None
        gross_income = gross_income_tag.text.strip() if gross_income_tag else None

        year_established_tag = soup.find("div", string="Year Established").find_next("div") if soup.find("div", string="Year Established") else None
        year_established = year_established_tag.text.strip() if year_established_tag else None

        employees_tag = soup.find("div", string="Employees").find_next("div") if soup.find("div", string="Employees") else None
        employees = employees_tag.text.strip() if employees_tag else None

        print(f"Details fetched for Listing ID {listing_id}:")
        print(f"Description: {description}")
        print(f"Gross Income: {gross_income}")
        print(f"Year Established: {year_established}")
        print(f"Employees: {employees}")

        # Check if details for this listing_id already exist
        cursor.execute("SELECT 1 FROM websiteclosers_details WHERE listing_id = %s", (listing_id,))
        if cursor.fetchone():
            print(f"Details already exist for Listing ID: {listing_id}, skipping...")
            continue

        # Insert the scraped details into the details table
        cursor.execute("""
            INSERT INTO websiteclosers_details (listing_id, description, gross_income, year_established, employees)
            VALUES (%s, %s, %s, %s, %s)
        """, (listing_id, description, gross_income, year_established, employees))
        conn.commit()
        print(f"Details inserted for Listing ID: {listing_id}")

if __name__ == "__main__":
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        scrape_details(cursor, conn)
    finally:
        cursor.close()
        conn.close()

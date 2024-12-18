import requests
from bs4 import BeautifulSoup
import psycopg2

# Database Configuration
DB_NAME = "scraping_demo"
DB_USER = "postgres"
DB_PASSWORD = "scrapingdemo"  # Same as in docker-compose.yml
DB_HOST = "localhost"
DB_PORT = "5433"  # Use 5433 instead of 5432


# Step 1: Set the target URL
url = "https://www.websiteclosers.com/businesses-for-sale/"

# Step 2: Connect to PostgreSQL Database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    print("✅ Database connection successful!")
except Exception as e:
    print("❌ Error connecting to the database:", e)
    exit()

# Step 3: Fetch the webpage
response = requests.get(url)
if response.status_code == 200:
    print("✅ Successfully fetched the webpage!")

    # Step 4: Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 5: Find all business listings
    listings = soup.find_all('div', class_='post_item')

    # Step 6: Extract and insert data into PostgreSQL
    for listing in listings:
        # Extract the link
        link_tag = listing.find('a', class_='post_thumbnail')
        link = link_tag['href'] if link_tag and link_tag.get('href') else None

        if link:
            try:
                # Insert the link into the database
                cursor.execute("INSERT INTO websiteclosers_listing (url) VALUES (%s)", (link,))
                conn.commit()  # Save changes
                print(f"✅ Inserted: {link}")
            except Exception as e:
                print(f"❌ Failed to insert data: {e}")
else:
    print(f"❌ Failed to fetch the webpage. Status code: {response.status_code}")

# Step 7: Close the database connection
cursor.close()
conn.close()
print("✅ Database connection closed.")



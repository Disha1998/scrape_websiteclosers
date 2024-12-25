import requests
from bs4 import BeautifulSoup

def clear_table(cursor, conn):
    cursor.execute("TRUNCATE TABLE websiteclosers_listing RESTART IDENTITY;")
    conn.commit()
    print("Table cleared successfully.")




import requests
from bs4 import BeautifulSoup

def scrape_website(cursor, conn):
    base_url = "https://www.websiteclosers.com/businesses-for-sale/page/{}/"
    page = 1  # Start with the first page
    has_more_pages = True
    total_scraped = 0  # Counter to track the total number of listings scraped

    while has_more_pages:
        print(f"Scraping page {page}...")
        url = base_url.format(page)
        response = requests.get(url)
        print(f"HTTP Response: {response.status_code}")

        if response.status_code != 200:
            raise Exception(f"Failed to fetch webpage. Status code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all('div', class_='post_item')

        if not listings:
            print("No more listings found. Exiting...")
            has_more_pages = False
            break

        for listing in listings:
            # Extract the link
            link_tag = listing.find('a', class_='post_thumbnail')
            link = link_tag['href'] if link_tag and link_tag.get('href') else None

            # Extract the title
            title_tag = listing.find('a', class_='post_title')
            title = title_tag.text.strip() if title_tag else None

            # Extract the description
            description_tag = listing.find('div', class_='the_content')
            description = description_tag.text.strip() if description_tag else None

            # Extract the asking price
            asking_price_tag = listing.find('div', class_='asking_price')
            asking_price = asking_price_tag.find('strong').text.strip() if asking_price_tag and asking_price_tag.find('strong') else None

            # Extract the cash flow
            cash_flow_tag = listing.find('div', class_='cash_flow')
            cash_flow = cash_flow_tag.find('strong').text.strip() if cash_flow_tag and cash_flow_tag.find('strong') else None

            print(f"Data fetched: {title}, {description}, {asking_price}, {cash_flow}, {link}")

            if link:
                cursor.execute("SELECT 1 FROM websiteclosers_listing WHERE url = %s", (link,))
                if not cursor.fetchone():  # Avoid duplicates
                    # Insert the data into the database
                    cursor.execute(
                        """
                        INSERT INTO websiteclosers_listing (url, title, description, asking_price, cash_flow)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (link, title, description, asking_price, cash_flow)
                    )
                    conn.commit()
                    total_scraped += 1  # Increment the counter

                    print(f"Inserted into DB: {link}")

        # Go to the next page
        page += 1
            # Print the total number of listings scraped

    print(f"Total listings scraped: {total_scraped}")
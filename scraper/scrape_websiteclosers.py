import requests
from bs4 import BeautifulSoup

def scrape_website(cursor, conn):
    
    url = "https://www.websiteclosers.com/businesses-for-sale/"
    response = requests.get(url)
    print(f"response ----- {response}")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch webpage. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all('div', class_='post_item')

    for listing in listings:
        link_tag = listing.find('a', class_='post_thumbnail')
        link = link_tag['href'] if link_tag and link_tag.get('href') else None
        print(f"listings of the links {link}")
        if link:
            cursor.execute("SELECT 1 FROM websiteclosers_listing WHERE url = %s", (link,))
            if not cursor.fetchone():  # Avoid duplicates
                cursor.execute("INSERT INTO websiteclosers_listing (url) VALUES (%s)", (link,))
                conn.commit()


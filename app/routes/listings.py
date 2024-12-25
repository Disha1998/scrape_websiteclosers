# This file will define FastAPI routes for scraping and accessing the database.

from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from scraper.scrape_websiteclosers import scrape_website

router = APIRouter()


# @router.post("/scrape")
# def start_scraping():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         scrape_website(cursor, conn)
#         cursor.close()
#         conn.close()
#         return {"message": "Scraping completed successfully!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



@router.get("/listings")
def get_listings():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM websiteclosers_listing")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{"id": row[0], "url": row[1], "title": row[2], "description": row[3], "asking_price": row[4], "cash_flow": row[5]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

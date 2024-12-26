from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter()

@router.get("/details/{id}")
def get_detail(id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Perform a JOIN query to fetch listing and detail data
        cursor.execute("""
            SELECT 
                d.id, d.listing_id, d.description AS detail_description, d.gross_income, 
                d.year_established, d.employees,
                l.url, l.title, l.asking_price, l.cash_flow
            FROM 
                websiteclosers_details d
            JOIN 
                websiteclosers_listing l
            ON 
                d.listing_id = l.id
            WHERE 
                d.id = %s
        """, (id,))
        
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Detail not found")
        
        # Map the result to a dictionary
        return {
            "id": row[0],
            "listing_id": row[1],
            "detail_description": row[2],  # Only detail description is kept
            "gross_income": row[3],
            "year_established": row[4],
            "employees": row[5],
            "url": row[6],
            "title": row[7],
            "asking_price": row[8],
            "cash_flow": row[9]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

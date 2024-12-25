from fastapi import FastAPI
from app.routes import listings

app = FastAPI()

app.include_router(listings.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Website Scraper API!"}

from fastapi import FastAPI
from app.routes import listings, details
app = FastAPI()

app.include_router(listings.router)
app.include_router(details.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Website Scraper API!"}

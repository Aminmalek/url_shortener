from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from cache import cache
from services import generate_short_url,get_url_by_short,create_short_url
from models import Base
from database import engine
from pydantic import BaseModel
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Define the request body using Pydantic
class URLRequest(BaseModel):
    user_id: int
    original_url: str

@app.post("/shorten/")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    # Check if short URL exists in cache
    short_url = generate_short_url(request.user_id, request.original_url)
    cached_url = cache.get(short_url)
    if cached_url:
        return {"short_url": cached_url}

    url = create_short_url(db, request.user_id, request.original_url, short_url)
    cache.set(short_url, request.original_url)
    return {"short_url": short_url}

@app.get("/{short_url}")
def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    # Cache aside architecture
    original_url = cache.get(short_url)
    if original_url:
        return {"original_url": original_url}

    # Fallback to DB if not in cache
    url = get_url_by_short(db, short_url)
    if url:
        cache.set(short_url, url.original_url)
        return {"original_url": url.original_url}

    raise HTTPException(status_code=404, detail="URL not found")

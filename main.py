from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from cache import cache
from database import engine
from database import get_db
from models import Base
from services import URLShortener

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Define the request body using Pydantic
class URLRequest(BaseModel):
    user_id: int
    original_url: str


@app.post("/shorten/")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    url_shortener = URLShortener(db)

    # First, try generating a unique short URL
    try:
        short_url = url_shortener.generate_short_url(request.user_id, request.original_url)
    except IntegrityError:
        short_url = url_shortener.shorten_url_with_retry(request.user_id, request.original_url)
    # Check if the short URL already exists in the cache
    cached_url = cache.get(short_url)
    if cached_url:
        return {"short_url": "firouze.shortener.com/" + short_url}

    # Cache the new short URL
    cache.set(short_url, request.original_url)

    return {"short_url": "firouze.shortener.com/" + short_url}


@app.get("/{short_url}")
def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    url_shortener = URLShortener(db)

    # Here I used cache aside pattern: First check cache
    original_url = cache.get(short_url)
    if original_url:
        return RedirectResponse(url=original_url)

    # Fallback to DB if not in cache
    url = url_shortener.get_url_by_short(short_url)
    if url:
        # Cache the original URL for future requests
        cache.set(short_url, url.original_url)
        return RedirectResponse(url=url.original_url)

    raise HTTPException(status_code=404, detail="URL not found")
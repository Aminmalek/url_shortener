import hashlib
from typing import Type

from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import URL


class URLShortener:
    MAX_RETRIES = 5  # Set the maximum number of retries

    def __init__(self, db: Session):
        self.db = db

    def shorten_url_with_retry(self, user_id: int, original_url: str) -> str:
        for attempt in range(self.MAX_RETRIES):
            try:
                short_url = self.generate_short_url(user_id, original_url)

                # Return existing short URL if it already exists
                existing_entry = self.get_existing_url(original_url)
                if existing_entry:
                    return existing_entry.short_url

                # Create a new entry in the database
                return self.create_new_entry(user_id, original_url, short_url)

            except IntegrityError:
                self.db.rollback()  # Rollback on collision

        raise HTTPException(status_code=500, detail="Unable to generate unique short URL after multiple attempts")

    def get_existing_url(self, original_url: str) -> Type[URL] | None:
        return self.db.query(URL).filter_by(original_url=original_url).first()

    def create_new_entry(self, user_id: int, original_url: str, short_url: str) -> str:
        new_entry = URL(user_id=user_id, original_url=original_url, short_url=short_url)
        self.db.add(new_entry)
        self.db.commit()
        return new_entry.short_url

    def is_short_url_unique(self, short_url: str) -> bool:
        """
        Helper function to check if a short URL is unique in the database.
        """
        existing_url = self.db.query(URL).filter_by(short_url=short_url).first()
        return existing_url is None

    @staticmethod
    def generate_short_url(user_id: int, original_url: str) -> str:
        """
        Generates a short URL using the SHA-256 hash.
        """
        hash_object = hashlib.sha256(f"{user_id}{original_url}".encode())
        hex_dig = hash_object.hexdigest()

        # Return the first 5 characters
        return hex_dig[:5]

    def get_url_by_short(self, short_url: str):
        """
        Retrieves a URL by the shortened version.
        """
        return self.db.query(URL).filter(URL.short_url == short_url).first()

    def create_short_url(self, user_id: int, original_url: str, short_url: str):
        """
        Creates a new short URL in the database.
        """
        db_url = URL(user_id=user_id, original_url=original_url, short_url=short_url)
        self.db.add(db_url)
        self.db.commit()
        self.db.refresh(db_url)
        return db_url

import hashlib
from sqlalchemy.orm import Session
from models import URL

import hashlib
import string

BASE62_ALPHABET = string.ascii_letters + string.digits  # a-zA-Z0-9 (62 characters)


def base62_encode(num: int) -> str:
    """Encodes a number into base62 (a-z, A-Z, 0-9)."""
    if num == 0:
        return BASE62_ALPHABET[0]

    encoded_str = []
    base = len(BASE62_ALPHABET)

    while num > 0:
        remainder = num % base
        encoded_str.append(BASE62_ALPHABET[remainder])
        num //= base

    return ''.join(reversed(encoded_str))


def generate_short_url(user_id: int, original_url: str) -> str:
    hash_object = hashlib.sha256(f"{user_id}{original_url}".encode())

    # Convert the hash to an integer
    hash_int = int(hash_object.hexdigest(), 16)

    base62_hash = base62_encode(hash_int)

    return base62_hash[:5]


def get_url_by_short(db: Session, short_url: str):
    return db.query(URL).filter(URL.short_url == short_url).first()

def create_short_url(db: Session, user_id: int, original_url: str, short_url: str):
    db_url = URL(user_id=user_id, original_url=original_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

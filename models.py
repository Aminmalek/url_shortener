from sqlalchemy import Column, Integer, String
from database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String(5), unique=True, index=True)

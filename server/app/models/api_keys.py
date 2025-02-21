from sqlalchemy import Column, Integer, String, Boolean
from server.app.db.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    rate_limit_per_minute = Column(Integer, default=60)
    status = Column(Boolean, default=True)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.app.core.config import DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add it to your local .env file.")

# The engine owns the PostgreSQL connection pool used by SQLAlchemy.
engine = create_engine(DATABASE_URL)

# Each backend operation should create a short-lived database session from this factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All SQLAlchemy table models inherit from Base so tables can be created from metadata.
Base = declarative_base()

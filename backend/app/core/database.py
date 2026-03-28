import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

# Load environment variables from the .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Get the database URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy Engine
# The engine is the core interface to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our models to inherit from
Base = declarative_base()

# Dependency to get the database session in our endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
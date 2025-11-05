from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# Replace with your actual database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Replace with your actual MongoDB connection string
MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(MONGO_CONNECTION_STRING)
db = client.get_database("qufin_db")
users_collection = db.get_collection("users")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
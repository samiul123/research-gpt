import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")  # Default region
    INDEX_NAME = os.getenv("INDEX_NAME", "research-gpt")
    CLOUD = os.getenv("CLOUD", "aws")
    EMBEDDING_DIMENSION = 1536
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")
    LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "logs")
    


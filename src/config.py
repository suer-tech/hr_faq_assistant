import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost/hr_db")
    COLLECTION_NAME = "hr_documents"

    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "openchat/openchat-7b")

    # Embeddings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "jinaai/jina-embeddings-v2-base-en")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
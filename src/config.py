import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost/hr_db")
    COLLECTION_NAME = "hr_documents"

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    # Embeddings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "jinaai/jina-embeddings-v2-base-en")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
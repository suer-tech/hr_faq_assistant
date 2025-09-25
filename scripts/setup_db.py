import logging
from sqlalchemy import create_engine, text
from config import Config

# Настройка логирования
logging.basicConfig(level=Config.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_db():
    logger.info("Проверяем подключение к базе данных...")
    try:
        engine = create_engine(Config.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            conn.commit()
            logger.info("pgvector extension enabled.")
        logger.info("Database ready.")
    except Exception as e:
        logger.error(f"Ошибка при подключении к базе: {e}")
        raise

if __name__ == "__main__":
    setup_db()
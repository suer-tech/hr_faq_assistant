import subprocess
import sys
import logging
from config import Config

# Настройка логирования
logging.basicConfig(level=Config.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_tests():
    logger.info("Запускаем тесты...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Тесты провалены:")
        logger.error(result.stdout)
        logger.error(result.stderr)
        sys.exit(1)
    else:
        logger.info("Тесты пройдены!")

if __name__ == "__main__":
    run_tests()
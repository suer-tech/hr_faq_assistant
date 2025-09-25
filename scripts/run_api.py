import uvicorn
from src.api.main import app
from config import Config

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=True
    )
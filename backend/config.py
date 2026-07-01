from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = (
        f"postgresql+asyncpg://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    DB_SCHEMA =os.getenv('DB_SCHEMA')
    
    API_URL = os.getenv('API_URL')
    
settings = Settings()
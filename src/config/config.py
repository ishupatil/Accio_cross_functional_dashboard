import os
from pathlib import Path
from dotenv import load_dotenv
from src.utils.logger import setup_logger

# Initialize a logger for the config module
logger = setup_logger("config")

# Get path to the workspace root directory (where .env is located)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load the environment variables from the .env file
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    logger.info(f"Loaded environment configuration from: {env_path}")
else:
    logger.warning(".env file not found. Falling back to environment variables.")

class Config:
    """
    Loads, validates, and stores application and database settings
    from environment variables.
    """
    def __init__(self) -> None:
        # PostgreSQL Database settings
        self.DB_HOST: str = os.getenv("DB_HOST", "localhost")
        
        # Cast DB_PORT to int with a safety check and default fallback
        try:
            self.DB_PORT: int = int(os.getenv("DB_PORT", 5432))
        except ValueError:
            logger.warning("Invalid DB_PORT environment variable; defaulting to 5432.")
            self.DB_PORT = 5432
            
        self.DB_NAME: str = os.getenv("DB_NAME", "retailmart_db")
        self.DB_USER: str = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
        self.DB_SCHEMA: str = os.getenv("DB_SCHEMA", "public")
        
        # Application settings
        self.APP_ENV: str = os.getenv("APP_ENV", "development")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Validate that essential credentials exist
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validates that essential settings are not empty."""
        missing = []
        if not self.DB_NAME:
            missing.append("DB_NAME")
        if not self.DB_USER:
            missing.append("DB_USER")
        if not self.DB_PASSWORD:
            missing.append("DB_PASSWORD")
            
        if missing:
            logger.critical(f"Missing required database settings: {', '.join(missing)}")
            raise ValueError(f"Missing required database configuration: {', '.join(missing)}")
            
    @property
    def database_uri(self) -> str:
        """
        Generates the standard PostgreSQL connection URI.
        If DATABASE_URL is set in environment (e.g. on Render), parses and returns it.
        """
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            # SQLAlchemy expects postgresql:// scheme instead of postgres://
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            return db_url
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Export a single config instance to reuse across the codebase (Singleton pattern)
config = Config()

from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from src.config.config import config
from src.utils.logger import setup_logger

# Initialize logger for database module
logger = setup_logger("database")

class DatabaseConnector:
    """
    Manages SQLAlchemy engine creation, database sessions, 
    and checks database connection status.
    """
    def __init__(self) -> None:
        self.connection_uri = config.database_uri
        self._engine: Engine = None
        self._session_factory = None
        
        # Initialize the engine
        self._initialize_engine()
        
    def _initialize_engine(self) -> None:
        """Initializes the SQLAlchemy engine and session factory."""
        try:
            # Create engine with connection pooling enabled
            self._engine = create_engine(
                self.connection_uri,
                pool_size=5,             # Maintain up to 5 connections
                max_overflow=10,         # Allow up to 10 temporary extra connections
                pool_timeout=30,         # Seconds to wait before giving up on a connection
                pool_recycle=1800,       # Recycle connections every 30 minutes
            )
            self._session_factory = sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False
            )
            logger.info("SQLAlchemy Database Engine initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize database engine: {e}")
            raise

    def get_engine(self) -> Engine:
        """
        Returns the SQLAlchemy engine instance.
        
        Returns:
            Engine: The active SQLAlchemy Engine.
        """
        if self._engine is None:
            self._initialize_engine()
        return self._engine

    def get_session(self) -> Session:
        """
        Creates and returns a new SQLAlchemy Session.
        Ensure you close the session after database operations.
        
        Returns:
            Session: A new database session transaction block.
        """
        if self._session_factory is None:
            self._initialize_engine()
        return self._session_factory()

    def get_db(self) -> Generator[Session, None, None]:
        """
        Dependency generator for sessions (useful in web context or pipelines).
        Yields a session and automatically closes it when finished.
        """
        session = self.get_session()
        try:
            yield session
        finally:
            session.close()

    def test_connection(self) -> bool:
        """
        Executes a simple query 'SELECT 1;' to verify database connectivity.
        
        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            engine = self.get_engine()
            # Establish temporary connection and execute a light query
            with engine.connect() as connection:
                # We use text() to write raw SQL safely in SQLAlchemy
                result = connection.execute(text("SELECT 1"))
                # Read the result to verify
                result.fetchone()
            logger.info(f"Database connection verified successfully on database: '{config.DB_NAME}'")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database connectivity test failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while testing database connection: {e}")
            return False

# Export a single connection manager instance (Singleton pattern)
db_connector = DatabaseConnector()

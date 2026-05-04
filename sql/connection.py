import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DBConnection:
    """
    Manages PostgreSQL database connections using SQLAlchemy.
    """
    def __init__(self):
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", "5432")
        self.database = os.getenv("DB_NAME", "perfumeria_db")
        
        self.connection_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self._engine = None

    def get_engine(self):
        """
        Creates and returns a SQLAlchemy engine.
        """
        if self._engine is None:
            try:
                self._engine = create_engine(self.connection_url)
                # Test the connection
                with self._engine.connect() as conn:
                    pass
                print(f"Connected to database: {self.database}")
            except SQLAlchemyError as e:
                print(f"Error connecting to the database: {e}")
                raise e
        return self._engine

# Singleton instance to be used across the project
db_manager = DBConnection()

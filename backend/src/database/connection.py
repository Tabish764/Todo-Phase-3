from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import AsyncAdaptedQueuePool
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConnection:
    def __init__(self):
        self._engine: Optional[AsyncEngine] = None
        self._database_url: Optional[str] = None

    @property
    def database_url(self) -> str:
        if not self._database_url:
            self._database_url = "postgresql+asyncpg://neondb_owner:npg_UNwVtq5m0HLo@ep-restless-salad-adv78p0z-pooler.c-2.us-east-1.aws.neon.tech/neondb"
        return self._database_url

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            
            parsed_url = urlparse(self.database_url)
            query_params = parse_qs(parsed_url.query)
            
            ssl_mode = query_params.pop('sslmode', [None])[0]
            
            # Rebuild the query string without sslmode
            new_query = urlencode(query_params, doseq=True)
            
            # Rebuild the URL
            new_url = urlunparse(
                (parsed_url.scheme, parsed_url.netloc, parsed_url.path, 
                 parsed_url.params, new_query, parsed_url.fragment)
            )

            connect_args = {}
            if ssl_mode:
                connect_args['ssl'] = ssl_mode

            self._engine = create_async_engine(
                new_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False,  # Set to True for debugging SQL queries
                connect_args=connect_args
            )
        return self._engine

    async def connect(self):
        """Initialize the database connection"""
        # Engine is created on first access to the property
        _ = self.engine

    async def disconnect(self):
        """Close the database connection"""
        if self._engine:
            await self._engine.dispose()
            self._engine = None


# Global database connection instance
db_connection = DatabaseConnection()
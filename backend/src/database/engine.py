"""Database engine and session setup for the Todo AI Chatbot application."""
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from src.config import settings

# Parse the database URL to handle SSL parameters
def get_database_url_and_connect_args():
    """Parse database URL and extract SSL parameters for connect_args."""
    parsed_url = urlparse(settings.database_url)
    query_params = parse_qs(parsed_url.query)
    
    # Extract sslmode and channel_binding from query params
    ssl_mode = query_params.pop('sslmode', [None])[0]
    channel_binding = query_params.pop('channel_binding', [None])[0]
    
    # Rebuild the query string without SSL params
    new_query = urlencode(query_params, doseq=True)
    
    # Rebuild the URL without SSL query params
    clean_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, 
         parsed_url.params, new_query, parsed_url.fragment)
    )
    
    # Build connect_args for SSL (asyncpg format)
    # For asyncpg, SSL is configured via connect_args['ssl'] as True/False or a dict
    connect_args = {}
    if ssl_mode:
        # For asyncpg, 'require' means we need SSL, so set ssl=True
        # asyncpg doesn't accept 'sslmode' as a parameter
        if ssl_mode.lower() in ('require', 'prefer', 'verify-ca', 'verify-full'):
            connect_args['ssl'] = True
        elif ssl_mode.lower() == 'disable':
            connect_args['ssl'] = False
        # For 'allow', we can leave it as default (False)
    
    return clean_url, connect_args

# Get clean URL and connect args
db_url, connect_args = get_database_url_and_connect_args()

# Create async engine
async_engine = create_async_engine(
    db_url,
    echo=settings.db_echo,  # Set to True for debugging
    connect_args=connect_args
)

# Create sync engine (for Alembic migrations)
sync_engine = create_engine(
    settings.database_url.replace("+asyncpg", ""),
    echo=settings.db_echo,  # Set to True for debugging
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with AsyncSession(async_engine) as session:
        yield session
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")

# Add the backend/src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import your models here to register them with SQLModel
from src.database.models import *  # noqa

# Alembic Config object
config = context.config

# Configure Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the database URL from environment variable - use sync driver for Alembic
database_url = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/taskdb"
)

# ONLY replace asyncpg → psycopg2 for Alembic (no ssl replacement!)
if database_url.startswith("postgresql+asyncpg://"):
    database_url = database_url.replace(
        "postgresql+asyncpg://",
        "postgresql://",
        1
    )

config.set_main_option("sqlalchemy.url", database_url)

# Metadata for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

from __future__ import with_statement
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.ext.declarative import declarative_base
from alembic import context

import sys
import os

# Add the parent directory to sys.path so that the database module can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import SQLALCHEMY_DATABASE_URL, Base  # Import your database URL and Base


# This is the Alembic Config object, which provides access to the .ini file
config = context.config

# Set up logging
fileConfig(config.config_file_name)

# Set up the target metadata (for autogeneration of migrations)
target_metadata = Base.metadata

# This function is used by Alembic to get the connection for running migrations
def run_migrations_offline():
    """Run migrations in 'offline' mode (without an actual database connection)"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode (with an actual database connection)"""
    connectable = create_engine(SQLALCHEMY_DATABASE_URL)  # This connects to your DB

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Check if Alembic is running in offline or online mode and call the appropriate function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

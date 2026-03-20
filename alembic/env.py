import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlmodel import SQLModel

# Fix import path for Docker
sys.path.append(os.getcwd())

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import models
import model

target_metadata = SQLModel.metadata


def get_database_url():
    return os.getenv("DATABASE_URL")


def run_migrations_offline():
    url = get_database_url()

    if url:
        config.set_main_option("sqlalchemy.url", url)

    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = get_database_url()

    if url:
        config.set_main_option("sqlalchemy.url", url)

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
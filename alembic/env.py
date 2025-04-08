import asyncio
import os
from logging.config import fileConfig

from alembic import context
from app.persistence.entities import Base
from sqlalchemy.ext.asyncio import create_async_engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

db_url = os.getenv("SQLALCHEMY_DATABASE_URL", "")
config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata


def run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(db_url, future=True)
    async with connectable.begin() as connection:
        await connection.run_sync(run_migrations)
    await connectable.dispose()


asyncio.run(run_migrations_online())

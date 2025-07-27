import asyncio
from logging.config import fileConfig
from pathlib import Path
from src.dependency.models import Base
from src.dependency.database import make_connection_string
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import fastapi_users_db_sqlalchemy.generics
from fastapi_users_db_sqlalchemy.generics import GUID

config = context.config

# Настраиваем логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Получаем асинхронный URL БД
database_url = make_connection_string()

# Устанавливаем метаданные для миграций
target_metadata = Base.metadata

async def run_async_migrations():
    """Выполнение миграций в асинхронном режиме"""
    # Создаем асинхронный движок
    engine = create_async_engine(database_url)

    async with engine.connect() as connection:
        # Выполняем синхронные операции миграции через run_sync
        await connection.run_sync(do_run_migrations)

    # Корректно закрываем движок
    await engine.dispose()


def do_run_migrations(connection):
    """Синхронная функция для выполнения миграций"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
        # Критически важные настройки для работы с fastapi-users
        include_schemas=True,
        include_object=lambda object, name, type_, reflected, compare_to: True,
        include_symbol=lambda name, _: "GUID" not in name,
        user_module_prefix="",
        user_module_prefixes=['fastapi_users_db_sqlalchemy.generics.'],
        user_module_imports={
            'fastapi_users_db_sqlalchemy.generics': ['GUID']
        }


    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск асинхронных миграций"""
    # Запускаем асинхронную функцию в event loop
    asyncio.run(run_async_migrations())

run_migrations_online()
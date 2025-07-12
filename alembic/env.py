import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Импортируем наши модули после добавления пути
from src.dependency.database import Base, make_connection_string

# Стандартная конфигурация Alembic
config = context.config

# Настраиваем логирование
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
        render_as_batch=True  # Важно для асинхронной работы
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск асинхронных миграций"""
    # Запускаем асинхронную функцию в event loop
    asyncio.run(run_async_migrations())


run_migrations_online()
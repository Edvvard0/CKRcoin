from typing import Annotated

from fastapi import Depends
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

from app.config import database_url

# Создание асинхронного движка для подключения к базе данных
engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session  # Возвращаем сессию для использования
        except Exception:
            await session.rollback()  # Откатываем транзакцию при ошибке
            raise
        finally:
            await session.close()  # Закрываем сессию


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True  # Абстрактный базовый класс, чтобы избежать создания отдельной таблицы

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

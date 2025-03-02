from functools import wraps
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Integer, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import database_url
from app.logger import logger

engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


def connection(isolation_level=None):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    if isolation_level:
                        await session.execute(
                            text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                        )

                    return await method(*args, session=session, **kwargs)

                except (SQLAlchemyError, Exception) as e:
                    await session.rollback()

                    if isinstance(e, SQLAlchemyError):
                        msg = "Database"
                    else:
                        msg = "Unknown"
                    msg += " Exp: Cannot add"
                    logger.error(msg, exc_info=True)
                    raise e

                finally:
                    await session.close()

        return wrapper

    return decorator


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session

        except (SQLAlchemyError, Exception) as e:
            await session.rollback()

            if isinstance(e, SQLAlchemyError):
                msg = "Database"
            else:
                msg = "Unknown"
            msg += " Exp: Cannot add"
            logger.error(msg, exc_info=True)
            raise e

        finally:
            await session.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    @property
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

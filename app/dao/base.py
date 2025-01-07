from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.database import SessionDep


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: SessionDep, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        blogs = result.scalars().all()
        return blogs

    @classmethod
    async def add(cls, session: SessionDep, **values):
        async with session.begin():
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance

    @classmethod
    async def find_one_or_none_by_id(cls, session: SessionDep, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: SessionDep, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update(cls, session: SessionDep, filter_by, **values):

        values = {k: v for k, v in values.items() if v is not None}

        if not values:
            return None

        async with session.begin():
            query = sqlalchemy_update(cls.model)\
                .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])\
                .values(**values)\
                .execution_options(synchronize_session="fetch")
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount

    @classmethod
    async def delete(cls, session: SessionDep, **filter_by):
        async with session.begin():
            query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount

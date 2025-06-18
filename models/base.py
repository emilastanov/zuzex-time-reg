import asyncio

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, joinedload

from services.db import SessionLocal

Base = declarative_base()


class CRUDMixin:
    @classmethod
    def _create(cls, **fields):
        try:
            with SessionLocal() as db:
                new_entity = cls(**fields)
                db.add(new_entity)
                db.commit()
                db.refresh(new_entity)

                return new_entity

        except SQLAlchemyError as e:
            raise ValueError(f"Failed to create {cls.__str__}: {str(e)}")

    @classmethod
    async def create(cls, **fields):
        return await asyncio.to_thread(cls._create, **fields)

    @classmethod
    def _find(cls, limit=25, offset=0, **filters):
        try:
            with SessionLocal() as db:
                query = db.query(cls)
                entities = query

                if filters:
                    conditions = [
                        getattr(cls, field_name) == value
                        for field_name, value in filters.items()
                    ]
                    entities = entities.filter(*conditions)

                entities = entities.limit(limit).offset(offset).all()

                total_count = query.count()

                return entities, total_count

        except SQLAlchemyError as e:
            raise ValueError(f"Failed to find {cls.__str__}: {str(e)}")

    @classmethod
    async def find(cls, limit=25, offset=0, **filters):
        return await asyncio.to_thread(cls._find, limit, offset, **filters)

    @classmethod
    def _find_one(cls, eager_load: list[str] = None, **filters):
        try:
            with SessionLocal() as db:
                query = db.query(cls)

                if eager_load:
                    for relation in eager_load:
                        query = query.options(joinedload(getattr(cls, relation)))

                conditions = [
                    getattr(cls, field_name) == value
                    for field_name, value in filters.items()
                ]

                entity = query.filter(*conditions).first()
                return entity

        except SQLAlchemyError as e:
            raise ValueError(f"Failed to find {cls.__name__}: {str(e)}")

    @classmethod
    async def find_one(cls, eager_load: list[str] = None, **filters):
        return await asyncio.to_thread(cls._find_one, eager_load, **filters)

    @classmethod
    def _update(cls, id, pk=None, **fields):
        try:
            with SessionLocal() as db:
                entity = (
                    db.query(cls).filter(getattr(cls, pk if pk else "id") == id).first()
                )

                for field_name, value in fields.items():
                    setattr(entity, field_name, value)

                db.commit()
                db.refresh(entity)

                return entity

        except SQLAlchemyError as e:
            raise ValueError(f"Failed to find {cls.__str__}: {str(e)}")

    @classmethod
    async def update(cls, id, pk=None, **fields):
        return await asyncio.to_thread(cls._update, id, pk, **fields)

    @classmethod
    def _delete(cls, id):
        try:
            with SessionLocal() as db:
                entity = db.query(cls).filter(getattr(cls, "id") == id).first()

                db.delete(entity)
                db.commit()

                return entity

        except SQLAlchemyError as e:
            raise ValueError(f"Failed to delete {cls.__str__}: {str(e)}")

    @classmethod
    async def delete(cls, id):
        return await asyncio.to_thread(cls._delete, id)

import uuid
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session


class CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]:
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, id: uuid.UUID) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)  # noqa
        return result.scalars().first()

    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_on desc",
    ) -> list[ModelType]:
        order_column_name, order_direction = order_by.split()
        order_column = getattr(self.model, order_column_name)
        order_expression = (
            desc(order_column)
            if order_direction.lower() == "desc"
            else asc(order_column)
        )
        query = (
            select(self.model)
            .order_by(order_expression)
            .where(self.model.is_available == bool(True))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)  # noqa
        return result.scalars().all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()  # noqa
        await db.refresh(db_obj)  # noqa
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()  # noqa
        await db.refresh(db_obj)  # noqa
        return db_obj

    async def remove(self, db: Session, *, id: uuid.UUID) -> ModelType:
        query = await self.get(db, id)
        await db.delete(query)  # noqa
        await db.commit()  # noqa
        return query

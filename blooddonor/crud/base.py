import uuid
from collections.abc import Sequence
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Row, RowMapping, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import joinedload


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
        query = (
            select(self.model)
            .options(joinedload(self.model.profile))
            .where(self.model.id == id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_on desc",
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        order_column_name, order_direction = order_by.split()
        order_column = getattr(self.model, order_column_name)
        order_expression = (
            desc(order_column)
            if order_direction.lower() == "desc"
            else asc(order_column)
        )
        query = (
            select(self.model)
            .options(joinedload(self.model.profile))
            .order_by(order_expression)
            .where(self.model.is_available == True)  # noqa
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
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
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if hasattr(db_obj, field) and isinstance(update_data[field], dict):
                    profile_obj = getattr(db_obj, field)
                    for pk, pv in update_data[field].items():
                        setattr(profile_obj, pk, pv)
                else:
                    setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, id: uuid.UUID) -> ModelType:
        query = await self.get(db, id)
        await db.delete(query)
        await db.commit()
        return query

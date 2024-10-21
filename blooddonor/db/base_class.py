from uuid import UUID

from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    metadata = None
    id: UUID
    __name__: str

    # Generate table name automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

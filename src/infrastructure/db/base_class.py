
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import ColumnProperty


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            attribute.key: getattr(self, attribute.key)
            for attribute in self.__mapper__.iterate_properties
            if isinstance(attribute, ColumnProperty)
        }
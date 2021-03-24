import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import CHAR
from sqlalchemy.types import TypeDecorator

def generate_uuid():
    return str(uuid.uuid4())

__all__ = [
    'GUID'
]

class GUID(TypeDecorator):
    """GUID column."""

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if not isinstance(value, uuid.UUID):
            try:
                return '%.32x' % int(uuid.UUID(value))
            except ValueError:
                return None
        else:
            return '%.32x' % int(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

    @staticmethod
    def gen_value():
        return uuid.uuid4()
import sqlalchemy as sa
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_all_tables(engine: sa.engine.Engine) -> None:
    Base.metadata.create_all(engine)


def recreate_all_tables(engine: sa.engine.Engine) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



class Organization(Base):
    __tablename__ = "organization"

    id = Column(sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()"))
    name = Column(sa.VARCHAR(255), nullable=False)
    slug = Column(sa.VARCHAR(255), nullable=False, unique=True)
    is_active = Column(sa.Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

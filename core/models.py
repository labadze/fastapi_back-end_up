import uuid

import sqlalchemy
from sqlalchemy import sql, DateTime, String, Boolean, ForeignKey, BigInteger, Integer, Enum, Float
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base, relationship

from core.database import Base


class User(Base):
    __tablename__ = 'users'
    id = uuid.UUID = sqlalchemy.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                       server_default=sql.func.gen_random_uuid(), nullable=False)
    created_at = sqlalchemy.Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = sqlalchemy.Column(DateTime(timezone=True), onupdate=sql.func.now())

    display_name = sqlalchemy.Column(String(64), nullable=False)

    user_name = sqlalchemy.Column(String(128), nullable=False, unique=True)

    ext_id = sqlalchemy.Column(String(512), nullable=False, unique=True)

    is_active = sqlalchemy.Column(Boolean, default=False)


class Item(Base):
    __tablename__ = 'items'
    id = uuid.UUID = sqlalchemy.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                       server_default=sql.func.gen_random_uuid(), nullable=False)
    created_at = sqlalchemy.Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = sqlalchemy.Column(DateTime(timezone=True), onupdate=sql.func.now())

    entry_value = sqlalchemy.Column(String(128), nullable=False, unique=True)

    is_active = sqlalchemy.Column(Boolean, default=False)

    rate = sqlalchemy.Column(Integer, default=False)

    carma = sqlalchemy.Column(Float, default=False)

    user_id = sqlalchemy.Column(postgresql.UUID(as_uuid=True),
                                ForeignKey("users.id", use_alter=True))
    user = relationship("User", back_populates="items", cascade="all, delete-orphan")


class DeadToken(Base):
    __tablename__ = 'dead_tokens'
    id = uuid.UUID = sqlalchemy.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                       server_default=sql.func.gen_random_uuid(), nullable=False)
    created_at = sqlalchemy.Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = sqlalchemy.Column(DateTime(timezone=True), onupdate=sql.func.now())

    user_id = sqlalchemy.Column(postgresql.UUID(as_uuid=True),
                                ForeignKey("users.id", use_alter=True))
    user = relationship("User", back_populates="items", cascade="all, delete-orphan")

    ext_id = sqlalchemy.Column(String(512), nullable=False, unique=True)

    token_value = sqlalchemy.Column(String(2048), nullable=False, unique=True)


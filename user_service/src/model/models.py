from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean, ARRAY, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, declarative_base, Mapped, relationship
from sqlalchemy.dialects.postgresql import JSONB
from passlib.context import CryptContext
from typing import Optional, List

pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")

class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), nullable=True)
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), default=func.now(), onupdate=func.now(), nullable=True)

class CustomUser(Base):
    __tablename__ = 'custom_user'

    name = Column(String(20))
    age = Column(Integer, nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    isactive = Column(Boolean, default=True)
    address = Column(JSONB, default={}, nullable=True)

    roles:Mapped[List['RoleMapping']] = relationship(uselist=True, lazy='selectin', back_populates='user', )

    def set_password(self, password):
        self.password = pwd_context.hash(password)
    
    def check_password(self, raw):
        return pwd_context.verify(raw, self.password)

class RoleMaster(Base):
    __tablename__ = 'role_master'

    name = Column(String, nullable = False, unique=True)
    description = Column(Text, nullable =True)

    users:Mapped[List['RoleMapping']] = relationship(uselist=True, back_populates='role')

class RoleMapping(Base):
    __tablename__ = 'role_mapping'

    user_id = Column(Integer, ForeignKey('custom_user.id'))
    role_id = Column(Integer, ForeignKey('role_master.id'))

    user : Mapped[Optional['CustomUser']] = relationship(back_populates='roles')
    role : Mapped[Optional['RoleMaster']] = relationship(back_populates='users')

    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='unique role mapping'),
    )




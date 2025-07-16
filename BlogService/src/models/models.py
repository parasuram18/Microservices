from sqlalchemy.orm import DeclarativeBase, MappedColumn
from sqlalchemy import Column, Integer, String, Text, DateTime, func, Boolean, ARRAY, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)
    modified_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True)


class BlogDetails(Base):
    __tablename__ = 'blog_details'

    title = Column(Text)
    content = Column(Text)
    author = Column(Integer)
    image = Column(JSONB, default={}, nullable=True)
    is_active = Column(Boolean, default=True)
    is_published = Column(Boolean, default=False)
    created_by = Column(Integer)
    modified_by = Column(Integer, nullable=True)

class LikeDetails(Base):
    __tablename__ = 'blog_like_details'

    blog_id = Column(Integer, ForeignKey('blog_details.id'))
    user_id = Column(Integer)
    is_liked = Column(Boolean)
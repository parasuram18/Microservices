from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import asdict
from ..models.models import *
from fastapi import HTTPException, status
from sqlalchemy import select, and_, or_, select
from sqlalchemy.orm import selectinload
from ..core.database import async_session


async def create_blog(input, info):
    db:AsyncSession = info.context['db']
    user = info.context['user']
    role = info.context['role']
    if role != "customer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not authenticated to perform this action")
    blogobj = BlogDetails(**asdict(input))
    db.add(blogobj)
    blogobj.author=user
    blogobj.created_by=user
    await db.commit()
    await db.refresh(blogobj)
    return blogobj

async def get_blogs(info):
    db:AsyncSession = info.context['db']
    role = info.context['role']
    user = info.context['user']
    if role == 'customer':
        stmt = select(BlogDetails).where(or_(BlogDetails.author==user, BlogDetails.is_active==True))
    else:
        stmt = select(BlogDetails).where(BlogDetails.is_active==True)

    result = await db.execute(stmt)
    blogobjs = result.scalars()
    return blogobjs

async def get_publish_count(id):
    async with async_session as db:
        stmt = select(BlogDetails).where(and_(BlogDetails.author==id, BlogDetails.is_published==True))
        result = db.execute(stmt)
        blogs = result.scalars()
        return len(blogs)

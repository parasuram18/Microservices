from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info, asdict
from ..models.models import *


async def create_blog(input, info):
    db:AsyncSession = info.context['db']
    blogobj = BlogDetails(**asdict(input))
    db.add(blogobj)
    blogobj.author=5
    blogobj.created_by=5
    await db.commit()
    await db.refresh(blogobj)
    return blogobj
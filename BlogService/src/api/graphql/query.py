import strawberry
from .types import *
from typing import List, Optional
from toolkit.toolkit.core import AuthenticateUser
from strawberry.types import Info
from ...services.blog_service import *

@strawberry.type
class Query:
    @strawberry.field
    async def GetBlogs(self, info:Info) -> List[Blog]:
        AuthenticateUser(info)
        return await get_blogs(info)
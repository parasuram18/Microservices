import strawberry
from .types import Blog, BlogInput
from strawberry.types import Info 
from ...services.blog_service import *
from toolkit.toolkit.core import AuthenticateUser

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def createblog(self, input:BlogInput, info:Info) ->Blog:
        AuthenticateUser(info)
        return await create_blog(input, info)
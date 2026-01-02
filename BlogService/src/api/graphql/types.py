import strawberry
from typing import Optional, List
from strawberry.federation import type, field
from strawberry import Private
from ...services.blog_service import *

@strawberry.federation.type(keys=['id'], extend=True)
class User:
    id : strawberry.ID = field(external=True)
    @strawberry.field
    async def publishes(self):
        await get_publish_count(self.id)
    publishes : Optional[int]



    # @staticmethod
    # def resolve_reference(id : strawberry.ID) -> "User":
    #     return User(id=id)

@strawberry.input
class BlogInput:
    title : str
    content : str

@strawberry.type
class Blog:
    id : int 
    title : str
    content : str
    image : str
    author: strawberry.ID
    @strawberry.federation.field(requires=["author"])
    def user(self) -> User:
        return User(id=self.author)


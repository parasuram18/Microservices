import strawberry
from typing import Optional, List
from strawberry.federation import type, field
from strawberry import Private
@strawberry.federation.type(keys=['id'], extend=True)
class User:
    id : strawberry.ID = field(external=True)

    # @staticmethod
    # def resolve_reference(id : strawberry.ID):
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
    author: User#strawberry.ID #Annotated[strawberry.ID, strawberry.Private]
    author: Private[strawberry.ID]  # not in the schema

    @strawberry.field                   # visible in schema
    def user(self) -> User:
        return User(id=self.author)
    # @strawberry.federation.field(requires=['author'])
    # async def authors(self) -> User:
    #     return User(id=self.author)


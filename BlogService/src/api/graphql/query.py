import strawberry
from .types import *
from typing import List, Optional

@strawberry.type
class Query:
    @strawberry.field
    async def get_blogs(self) -> Blog:
        return Blog(id=1,title='my first blog', content='about sports', image={}, author=1)
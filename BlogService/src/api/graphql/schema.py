from .query import Query
from .mutation import Mutation
from strawberry.federation import Schema


schema = Schema(query=Query, mutation=Mutation)
# main.py
from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from .src.api.graphql.schemas import schema
from .src.core.database import Session
import jwt
from .src.core import config




async def get_context(session:Session):
        return {"db": session}

# async def get_context(request:Request):
#     db_gen=async_get_db()
#     db=await db_gen.__anext__()
#     try:
#         yield {"db": db}
#     finally:
#         await db_gen.aclose()
 
 
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

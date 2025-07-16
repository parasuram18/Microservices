from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from src.api.graphql.schema import schema
from src.core.database import session

def get_context(session:session):
    return {"db":session}

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)
app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")
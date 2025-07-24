from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from src.api.graphql.schema import schema
from src.core.database import async_session

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with async_session() as session:
        request.state.db = session
        response = await call_next(request)
        return response
    
def get_context(request:Request):
    # session : AsyncSession = async_session()
    return {"db":request.state.db}

graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
async def root():
    return {"status":"ok"}
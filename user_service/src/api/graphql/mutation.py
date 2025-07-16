import strawberry
from .types import *
from dataclasses import asdict
from ...services.user_services import *
from ...core.database import Session
from strawberry import Info

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_roles(self, input:RoleInp, info:Info) -> RoleRes:
        AuthenticateUser(info)
        return await add_role(input,info)

    # @strawberry.mutation
    # async def register(self, input:UserInput, info:Info) -> User:
    #     return await register_user(input, info)
    
    @strawberry.mutation
    async def login(self, input:LoginData, info:Info) -> LoginRes:
        return LoginRes(token_type=config.JWT_AUTH_HEADER_PREFIX, access_token=await login_user(input, info))
import strawberry
from .types import *
from strawberry.types import Info
from ...services.user_services import *
# from ...services.auth import AuthenticateUser
from toolkit.toolkit.core import AuthenticateUser
# from toolkit import toolkit
@strawberry.type
class Query:
    @strawberry.field
    async def get_roles(self, info:Info) -> List[RoleRes]:
        print(info.context['request'].headers)
        AuthenticateUser(info)
        return await get_roles(info)
    
    # @strawberry.field
    # async def ex_user(self, id:strawberry.ID) -> ExUser:
    #     return await ExUser(id=id, email='parasu@gmail.com')
    
    @strawberry.field
    async def get_user(self, info:Info) -> List[User]:
        AuthenticateUser(info)
        return await get_user(info) 
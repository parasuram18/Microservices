import strawberry
from typing import Optional, List, Union
from enum import Enum
from strawberry import Info
from ...services.user_services import *
from strawberry.scalars import JSON
from ...core.database import Session, AsyncSessionLocal
class Roles(Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'

@strawberry.input
class RoleInp:
    name : str
    description : str
@strawberry.type
class RoleRes:
    id : int
    name : str

@strawberry.input
class AddressInp:
    district : Optional[str] = None
    pincode : Optional[str] = None

@strawberry.input
class UserInput:
    name : Optional[str] = None
    age : Optional[int] = None
    email : str
    password : str
    address: Optional[AddressInp] = None
    role : Roles

@strawberry.type
class Address:
    district : Optional[str] = None
    pincode : Optional[str] = None

@strawberry.federation.type(keys=['id'])
class User:
    id : strawberry.ID
    name : Optional[str] = None
    email : str
    age : Optional[int] = None
    address: Optional[Address] = None

    @strawberry.field
    async def role(self)->RoleRes:
        return await get_role(self.id)
    
    @staticmethod
    async def resolve_reference(id:strawberry.ID) -> "User":
        user = await user_resolver(id)
        if user:
            return User(id=user.id, name=user.name, email=user.email, age=user.age, address=user.address)
    
@strawberry.input
class LoginData:
    email:str
    password:str

@strawberry.type
class LoginRes:
    token_type : str
    access_token : str


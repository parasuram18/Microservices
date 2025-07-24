from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import Info, asdict
from sqlalchemy import select, insert, update, delete, and_, or_
from ..model.models import *
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from .auth import *
from graphql import GraphQLError
import traceback
from ..core.database import AsyncSessionLocal, Session
# auth_user = 


async def get_roles(info:Info):
    role = info.context['role']
    if role not in ['admin']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not authenticat to perform this action')
    db:AsyncSession = info.context['db']
    stmt = select(RoleMaster)
    role_objs = await db.scalars(stmt)

    return role_objs

async def add_role(input:dict, info:Info):
    try:
        db:AsyncSession = info.context['db']

        stmt = select(RoleMaster).where(RoleMaster.name==input.name)
        role_obj = await db.scalar(stmt)
        if role_obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Role already exists')

        print(input, type(input))
        role_obj = RoleMaster(**asdict(input))
        db.add(role_obj)
        await db.commit()
        await db.refresh(role_obj)
        return role_obj
    except HTTPException as error:
        return error
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Role already exists')

async def register_user(input, info:Info):
    try:
        db:AsyncSession = info.context['db']
        input_data = asdict(input)   # returns a dict
        input_data.pop("role", None)  # remove role
        # userobj = CustomUser(**data)
        stmt = select(RoleMaster).where(RoleMaster.name==input.role.value)
        roleobj = await db.scalar(stmt)
        valid = (await db.execute(select(CustomUser).where(CustomUser.email==input.email))).scalar_one_or_none()
        if valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"status":"Error","message":"Email already Exists",})

        userobj = CustomUser(**input_data)
        userobj.set_password(input.password)
        db.add(userobj)
        await db.flush()
        maprole = RoleMapping(role_id=roleobj.id, user_id=userobj.id)
        db.add(maprole)
        await db.commit()
        await db.refresh(userobj)
        await db.refresh(maprole)

        return userobj
    except HTTPException as error:
        return error
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={
                                "status":"Error",
                                "message":str(e),
                            })

async def get_user(info:Info):
    try:
        db:AsyncSession = info.context['db']
        role = info.context['role']
        if role == 'customer':
            id = info.context['user']
            stmt = select(CustomUser).options(selectinload(CustomUser.roles)).where(CustomUser.id==id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            return [user]
        else:
            stmt = select(CustomUser)
            result = await db.execute(stmt)
            return result.scalars()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("......", str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")

async def get_role(id):
    async with AsyncSessionLocal() as db:
        stmt = select(RoleMapping).options(selectinload(RoleMapping.user), selectinload(RoleMapping.role)).where(RoleMapping.user_id==id)
        result = await db.execute(stmt)
        role = result.scalar_one_or_none()
        return role.role

async def get_users_per_role(role_id, info):
    db:AsyncSession = info.context['db']
    stmt = select(RoleMapping).options(selectinload(RoleMapping.user), selectinload(RoleMapping.role)).where(RoleMapping.role_id==role_id)
    users = await db.scalars(stmt)
    return users

async def login_user(input, info):
    db:AsyncSession = info.context['db']

    result = await db.execute(select(CustomUser).options(selectinload(CustomUser.roles)).where(CustomUser.email==input.email))
    userobj = result.scalar_one_or_none()
    if userobj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"User not found"})
    if not userobj.check_password(input.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Incorrect password"})
    return await generate_token(userobj, info)

async def user_resolver(id):
    async with AsyncSessionLocal() as db:
            stmt = select(CustomUser).where(CustomUser.id==int(id))
            result = await db.execute(stmt)
            return result.scalar_one_or_none()


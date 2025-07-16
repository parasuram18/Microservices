from jose import jwt, ExpiredSignatureError, JWTError
from ..model.models import CustomUser, RoleMaster
import time
from datetime import datetime, timedelta
from ..core import config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from strawberry.types import Info

async def payload_handler(userobj:CustomUser, info):
    db:AsyncSession = info.context['db']
    stmt = select(RoleMaster).where(RoleMaster.id==userobj.roles[0].role_id)
    result = await db.execute(stmt)
    roleobj = result.scalar_one_or_none()

    payload = {
        "id":userobj.id,
        "email":userobj.email,
        "role": roleobj.name, 
        "iat": time.time(),
        "exp":datetime.utcnow() + timedelta(seconds=int(config.JWT_EXPIRE_TIME))
    }
    return payload

async def generate_token(obj, info):
    try:
        payload = await payload_handler(obj, info)
        token = jwt.encode(payload, config.SECRET_KEY, config.JWT_ALGORITHM)
        return token
    except:
        return None

# def validate_token(info):
#     request = info.context['request']
#     token = request.headers.get('Authorization')
#     if not token or not token.startswith('Bearer'):
#         raise HTTPException(404, "Authentication credentials were Not Found")
#     token = token.split(' ')[1]
#     try:
#         payload = jwt.decode(token, config.SECRET_KEY, [config.JWT_ALGORITHM])
#         return payload
#     except ExpiredSignatureError:
#         raise HTTPException(404, "Token Expired")
#     except JWTError:
#         raise HTTPException(404, "Invalid Token")
        
# def AuthenticateUser(info):
#     payload = validate_token(info)
#     info.context['user'] = payload.get('id')
#     info.context['role'] = payload.get('role')
#     print( info.context['user'])


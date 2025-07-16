from fastapi.exceptions import HTTPException
from jose import jwt, ExpiredSignatureError, JWTError

SECRET_KEY = "$id$v=19$m=65536,t=3,p=4$CWcMeoDuZlQIzOW8Jf5bQg$UwCB+YsV9A+9aRSsObKejhJaavt28Xy12ig2lzvcg8M"
JWT_ALGORITHM = 'HS256'

def validate_token(info):
    request = info.context['request']
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer'):
        raise HTTPException(404, "Authentication credentials were Not Found")
    token = token.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, [JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(404, "Token Expired")
    except JWTError:
        raise HTTPException(404, "Invalid Token")
        
def AuthenticateUser(info):
    payload = validate_token(info)
    info.context['user'] = payload.get('id')
    info.context['role'] = payload.get('role')
    print( info.context['user'])
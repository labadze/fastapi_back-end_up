from fastapi import Depends, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from core.schemas import User, UserBase, UserInsert
from core.utils import decode_token
from db.db_ops import fetch_user_by_ext_id, insert_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    insert_result = str()
    decode_token_result = await decode_token(token)
    json_result = jsonable_encoder(decode_token_result)
    user_in_db_result = await fetch_user_by_ext_id(ext_id=decode_token_result.sub)
    if user_in_db_result is None:
        user_insert_data = UserInsert(
            ext_id=decode_token_result.sub,
            user_name=decode_token_result.preferred_username,
            display_name=decode_token_result.preferred_username,
            is_active=True,
        )
        insert_result: str = await insert_user(data=user_insert_data)
    user: User = User(
        id=user_in_db_result is None if insert_result else user_in_db_result.id,
        ext_id=decode_token_result.sub,
        display_name=decode_token_result.preferred_username,
        roles=decode_token_result.realm_access.roles,
        is_active=False,
        user_name=decode_token_result.preferred_username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

from fastapi import HTTPException


from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import users
from config.db_config import get_db


#根据token查询用户如何返回；门卫检查通行证。
async def get_current_user(
        authorization: str=Header(...,alias="Authorization"),
        db:AsyncSession = Depends(get_db)
):
    token =authorization.replace("Bearer ","")
    user =await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效令牌或者已经过期")

    return user
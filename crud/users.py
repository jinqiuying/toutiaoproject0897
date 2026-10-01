import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserRequest, UserUpdateRequest
from models.users import User, UserToken
from utils import security



#查询数据库的用户
async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user



#创建用户
async def create_user(db: AsyncSession, user_data:UserRequest):
    #密码加密
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

#生成token
async def create_token(db: AsyncSession, user_id: int):
    #设置过期时间，没有token就生成，有就更新
    token = str(uuid.uuid4())
    token_expires = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token :
        user_token.token = token
        user_token.expires_at = token_expires

    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=token_expires)
        db.add(user_token)

    await db.commit()
    return token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db,username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None

    return user

#根据token查用户
async def get_user_by_token(db: AsyncSession, token: str):
    result = await db.execute(select(UserToken).where(UserToken.token == token))
    user_token = result.scalar_one_or_none()
    if not user_token or user_token.expires_at < datetime.now():
        return None
    result2 = await db.execute(select(User).where(User.id == user_token.user_id))
    user = result2.scalar_one_or_none()
    return user


#更新用户信息
async def update_user(db: AsyncSession, user_name: str, user_data:UserUpdateRequest):
    result = await db.execute(update(User).where(User.username == user_name).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    ))
    await db.commit()
    #如果没有命中数据抛出异常
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    #返回更新后的用户信息
    result2 = await get_user(db,user_name)
    return result2


#更新用户密码
async def update_user_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False
    new_password_hash = security.get_hash_password(new_password)
    user.password = new_password_hash
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True


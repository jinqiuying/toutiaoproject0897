from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import users
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserPasswordUpdateRequest

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
#验证用户是否存在，创建用户，生成token，响应结果
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    exit_users = await users.get_user(db, user_data.username)
    if exit_users:
        raise HTTPException(status_code=400, detail="用户名已经存在")
    new_users = await users.create_user(db, user_data)
    token = await users.create_token(db, new_users.id)

    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo":{
    #             "id": new_users.id,
    #             "username": new_users.username,
    #             "bio": new_users.bio,
    #             "avatar": new_users.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(new_users))
    return success_response(message="注册成功",data = response_data)



@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 验证用户是否存在，密码是否正确，生成token，响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功", data=response_data)


@router.get("/info")

async def get_user_info(user:User=Depends(get_current_user)):
#查用户的token，封装，工具函数，导入
    return success_response(
        message="获取用户信息成功",
        data=UserInfoResponse.model_validate(user)
    )

@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):

    user_info = await users.update_user(db, user.username, user_data)
    return success_response(
        message="更新用户信息成功",
        data=UserInfoResponse.model_validate(user_info)
    )

@router.put("/password")
async def update_user_password(
        password_data:UserPasswordUpdateRequest,user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)
):
   update_password =  await users.update_user_password(db, user, password_data.old_password, password_data.new_password)
   if not update_password:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败")
   return success_response(message="修改密码成功")
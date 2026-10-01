import traceback

from fastapi import HTTPException,Request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi.responses import JSONResponse
from starlette import status

DEBUG_MODE = True

#处理HTTPException错误
async def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

#处理数据完整性错误
async def integrity_error_handler(request:Request,exc:IntegrityError) :
    error_msg = str(exc.orig)

    if "username_UNIQUE" in error_msg or "phone_UNIQUE" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN_KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据越是冲突，请检查输入"

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type":"IntegrityError",
            "error_detail":error_msg,
            "path":str(request.url)
        }


    return JSONResponse(
        status_code=status.HTTP_400BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )

async def sqlalchemy_exception_handler(request:Request,exc:SQLAlchemyError) :
    error_data =None
    if DEBUG_MODE:
        error_data = {
            "error_type":type(exc).__name__,
            "error_detail":str(exc),
            "path":str(request.url),
            "traceback":traceback.format_exc()
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message":"数据库操作失败，请稍后重试",
            "data": error_data
        }
        )

#处理所有未捕获的异常

async def general_exception_handler(request:Request,exc:Exception) :
    error_data =None
    if DEBUG_MODE:
        error_data = {
            "error_type":type(exc).__name__,
            "error_detail":str(exc),
            "path":str(request.url),
            "traceback":traceback.format_exc()
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message":"服务器内部错误",
            "data": error_data
        }
        )
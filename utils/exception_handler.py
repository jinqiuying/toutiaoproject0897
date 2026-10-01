from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_exception_handler, \
   general_exception_handler


def register_exception_handler(app):
   """
   注册异常处理
   :param app:
   :return:
   """
   app.add_exception_handler(HTTPException, http_exception_handler)#业务层
   app.add_exception_handler(IntegrityError, integrity_error_handler)#数据完整性约束
   app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)#数据库操作
   app.add_exception_handler(Exception, general_exception_handler)#所有未捕获的异常；兜底

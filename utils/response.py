from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(message: str="Success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
#把任何的对象都正常返回
    return JSONResponse(content = jsonable_encoder(content))

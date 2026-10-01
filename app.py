from fastapi import FastAPI

from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handler import register_exception_handler

app = FastAPI()
#注册异常处理器
register_exception_handler(app)

# ========= 解决跨域 =========
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],  # 只允许特定前端访问
    allow_origins=["*"],                          # 允许所有前端访问（开发阶段用）
    allow_credentials=False,                        # 允许带Cookie
    allow_methods=["*"],                           # 允许所有请求方式（GET/POST/PUT/DELETE...）
    allow_headers=["*"],                           # 允许所有请求头
)
# ==========================


@app.get('/')
def hello_world():  # put application's code here
    return 'Hello World!'




#挂载注册路由
app.include_router(news.router)
app.include_router(users.router)

app.include_router(favorite.router)

app.include_router(history.router)






if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)


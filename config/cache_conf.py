import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST ="192.168.1.7"
REDIS_PORT =6379
REDIS_DB = 0


#创建连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True#自动将返回值进行解码为字符串
)

#设置缓存和读取,读字符串
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None

#读字符串;读取：列表或字典（序列化）
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)#序列化
        return None
    except Exception as e:
        print(f"获取JSON缓存失败：{e}")
        return None

#设置缓存
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            value = json.dumps(value,ensure_ascii=False)#保留中文
        await redis_client.set(key,value,ex=expire)
        return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False


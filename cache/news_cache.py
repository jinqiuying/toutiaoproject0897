#新闻相关的缓存方法：新闻分类的读取和写入
from typing import Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list"

#获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

#写入新闻分类缓存:缓存的数据和过期的时间,分类，配置7200，列表600，详情1800，验证码120，数据越稳定越持久
#避免所有的key同时过期，引起缓存雪崩
async def set_cached_categories(data:list[dict[str,Any]],expire:int=7200):
    return await set_cache(CATEGORIES_KEY,data,expire)


#写入缓存-新闻列表 key = news_list:分类ID，页码：每页的数量+列表数据+过期时间
async def set_cached_news_list(category_id:Optional[int],page:int,page_size:int,data:list[dict[str,Any]],expire:int=7200):
    #调用封装的redis的设置方法，存新闻列表到缓存
    category_part =category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await set_cache(key,data,expire)

#读取缓存-新闻列表
async def get_cached_news_list(category_id:Optional[int],page:int,page_size:int):
    category_part =category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await get_json_cache(key)

#写入缓存-新闻详情，key =news_detail:新闻ID，数据+过期时间
async def set_cached_news_detail(news_id:int,data:dict[str,Any],expire:int =1800):
    key =f"news_detail:{news_id}"
    return await set_cache(key,data,expire)

#读取缓存-新闻详情
async def get_cached_news_detail(news_id:int):
    key = f"news_detail:{news_id}"
    return await get_json_cache(key)


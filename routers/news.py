from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  update

from cache import news_cache
from config.cache_conf import redis_client
from config.db_config import get_db
from crud import news
from models.news import NewsList

#创建APIRounter实例,prefix前缀,tags标签,description描述

router = APIRouter(prefix="/api/news",tags=["news"])

#接口实现流程
# 1. 模块化路由->API接口规范文档
# 2. 定义模型类->数据库表（数据库设计文档）
# 3. 在crub文件里面创建文件，封装操作数据库的方法
# 4. 在路由处理函数里面调用crub封装好的方法，响应结果




#路由函数



@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 获取数据库新闻分类列表数据，先定义模型类，封装查询数据的方法
    #调用查询方法,db注入依赖
    news_categories = await news.get_categories(db,skip,limit)
    return {
        "code": 200,
        "message": "success",
        "data": news_categories
    }


@router.get("/list")
async def get_news_list(
        category_id: int = Query( ..., alias= "categoryId" ),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize",le=100),
        db: AsyncSession = Depends(get_db)
):
    offset = (page -1) * page_size
    news_list = await news.get_news_list(db,category_id,offset,page_size)
    total_count = await news.get_news_list_count(db,category_id)
    has_more = total_count > (offset + len(news_list))
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": news_list,
            "total": total_count,
            "hasMore": has_more
        }
    }


@router.get("/detail")
async def get_news_detail(id: int = Query(alias="id"), db: AsyncSession = Depends(get_db)):
    detail = await news.get_news_detail(db, id)
    if detail is None:
        raise HTTPException(status_code=404, detail="新闻不存在")
    views = await news.increase_views(db, id)
    if views is None:
        raise HTTPException(status_code=404, detail="新闻不存在")
    relatedNews = await news.get_related_news(db, detail.id, detail.category_id)
    if relatedNews is None:
        raise HTTPException(status_code=404, detail="相关新闻不存在")
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": detail.id,
            "title": detail.title,
            "content": detail.content,
            "image": detail.image,
            "publishTime": detail.publish_time,
            "author": detail.author,
            "categoryId": detail.category_id,
            "views": detail.views,
            "relatedNews": [
                {"id": r.id,
                 "title": r.title,
                 "image": r.image,
                 "author": r.author,
                 "publishTime": r.publish_time,
                 "views": r.views
                 }
                for r in relatedNews
            ]
        }
    }



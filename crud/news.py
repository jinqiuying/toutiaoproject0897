from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cached_categories, get_cached_news_list, set_cached_news_list, \
    get_cached_news_detail, set_cached_news_detail
from models.base import NewsItemBase
from models.news import NewsCategory
from models.news import NewsList


#封装查询新闻的方法

#数据库会话
async def get_categories(db:AsyncSession,skip: int = 0, limit: int = 100):
    #先尝试从缓存获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    result = await db.execute(select(NewsCategory).offset(skip).limit(limit))
    categories =  result.scalars().all()#orm结果
    #写入缓存
    if categories:
        categories = jsonable_encoder(categories)#转orm为list
        await set_cached_categories(categories)#接收list和dict
    #返回数据
    return categories

async def get_news_list(db:AsyncSession,category_id: int, skip: int = 0, limit: int = 10):
    #先尝试从缓存获取新闻列表,分类，页码，每页数量
    page = skip//limit+1
    cached_list = await get_cached_news_list(category_id,page,limit)#缓存数据是json格式
    if cached_list:
        return [NewsList(**item) for item in cached_list]#将json格式数据转为NewsList对象
    result = await db.execute(select(NewsList).where(NewsList.category_id == category_id).offset(skip).limit(limit))
    news_list = result.scalars().all()

    #写入缓存
    if news_list:
     #orm转为pydantic，在转为字典,by_alias不适用别名，保存pydantic风格，因为redis数据是给后段用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False)for item in news_list]
        await set_cached_news_list(category_id,page,limit,news_data)
    #返回
    return news_list
#聚合函数，返回只能有一个结果，否则会报错
async def get_news_list_count(db:AsyncSession,category_id: int):
    result = await db.execute(select(func.count(NewsList.id)).where(NewsList.category_id == category_id))
    return result.scalar_one_or_none()


async def get_news_detail(db: AsyncSession, news_id: int):
    print(f"--- 开始查询 news_id={news_id} ---")

    # 读缓存
    cached = await get_cached_news_detail(news_id)
    print(f"1. 缓存结果: {cached}")

    if cached:
        print("2. 命中缓存，直接返回")
        views = await db.execute(select(NewsList.views).where(NewsList.id == news_id))
        cached["views"] = views.scalar_one_or_none()
        return NewsList(**cached)

    # 查数据库
    result = await db.execute(select(NewsList).where(NewsList.id == news_id))
    news = result.scalar_one_or_none()
    print(f"3. 数据库结果: {news is not None}")

    if news:
        try:
            news_data = NewsItemBase.model_validate(news).model_dump(mode="json")
            print(f"4. 转换成功: {type(news_data)}")
            news_data.pop("views")
            await set_cached_news_detail(news_id, news_data)
            print("5. ✅ 缓存写入成功")
        except Exception as e:
            print(f"5. ❌ 写入缓存失败: {e}")
        return news

    print("3. 数据库没查到，返回 None")
    return None

async def increase_views(db:AsyncSession, news_id:int):
    # 2. 浏览量+1
    result = await db.execute(
        update(NewsList).where(NewsList.id == news_id).values(views=NewsList.views + 1)
    )
    await db.commit()
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):

    # 3. 查询同分类的相关新闻（排除当前这条，取5条）
    related_result = await db.execute(
        select(NewsList)
        .where(NewsList.category_id == category_id, NewsList.id != news_id)
        .order_by(NewsList.views.desc(),NewsList.publish_time.desc())
        .limit(limit)
    )
    return related_result.scalars().all()

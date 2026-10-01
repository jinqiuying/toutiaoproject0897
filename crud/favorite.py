from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import NewsList


async def get_check_favorite(news_id: int, user_id: int, db: AsyncSession):
    """
    检查用户是否收藏了该新闻
    :param news_id:
    :param user_id:
    :param db:
    :return:是否有收藏记录，布尔值
    """
    result = await db.execute(select(Favorite).where(Favorite.user_id==user_id).where(Favorite.news_id==news_id))
    return result.scalar_one_or_none() is not None

async def add_news_favorite(news_id:int,user_id:int,db: AsyncSession):
    favorite = Favorite(user_id = user_id,news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(news_id: int,user_id:int, db: AsyncSession):
    """
    删除收藏
    :param news_id:
    :param user_id:
    :param db:
    :return:
    """
    # result = await db.execute(select(Favorite).where(Favorite.user_id==user_id).where(Favorite.news_id==news_id))
    # favorite = result.scalar_one_or_none()
    # if favorite is None:
    #     return False
    # await db.delete(favorite)
    # await db.commit()
    # return True
    result = await db.execute(delete(Favorite).where(Favorite.user_id==user_id).where(Favorite.news_id==news_id))
    await db.commit()
    return result.rowcount > 0

#总量+收藏新闻列表
async def get_favorite_list(
        db: AsyncSession,
        user_id:int,
        page:int=1,
        page_size:int=10
        ):
    """
    获取收藏列表
    :param db:
    :param user_id:
    :param page:
    :param pagesize:
    :return:
    """
    count_result = await db.execute(
        select(func.count())
        .where(Favorite.user_id==user_id))
    total = count_result.scalar_one()#总数量
    # result = await db.execute(
    #   select(NewsList,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
    #  .join(Favorite.user_id==user_id)
    #  .order_by(Favorite.created_at.desc())
    #  .offset((page-1)*page_size)
    #  .limit(page_size))  #联表查询+收藏时间排序+分页
    # rows = result.all()
    # return rows, total
    result = await db.execute(select( NewsList,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id")
    )
    .join(Favorite, Favorite.news_id == NewsList.id)  # ← 关联的表 + 关联条件
    .where(Favorite.user_id == user_id)               # ← 过滤条件放 where 里
    .order_by(Favorite.created_at.desc())
    .offset((page - 1) * page_size)
    .limit(page_size)
)
    rows = result.all()
    return rows, total

async def clear_favorite( user_id: int, db: AsyncSession):
    result = await db.execute(delete(Favorite).where(Favorite.user_id==user_id))
    await db.commit()
    return result.rowcount or 0

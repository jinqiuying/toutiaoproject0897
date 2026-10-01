from datetime import datetime

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import NewsList


async def get_check_history(db: AsyncSession,news_id:int,user_id:int):
    result =  await db.execute(select(History).where(History.news_id == news_id).where(History.user_id == user_id))
    return result.scalar_one_or_none() is not None

async def add_history(db: AsyncSession, user_id: int, news_id: int):
    # 1. 先去数据库查有没有浏览过
    result = await db.execute(
        select(History)
        .where(History.user_id == user_id)
        .where(History.news_id == news_id)
    )
    history = result.scalar_one_or_none()  # 查到了就是对象，查不到就是 None


    if history:
        history.view_time = datetime.now()
        await db.commit()
        await db.refresh(history)
        return history


    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history

async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10):
    #查总浏览量
    count_result = await db.execute(select(func.count()).where(History.user_id == user_id))
    total = count_result.scalar_one() or 0

    #联表查询（新闻表+历史浏览表）+浏览时间排序+分页
    result = await db.execute(select(NewsList,History.view_time.label("history_time"),History.id.label("history_id"))
     .join(History,NewsList.id == History.news_id)
     .where(History.user_id == user_id)
     .order_by(History.view_time.desc())
     .offset((page-1)*page_size)
     .limit(page_size)
     )
    rows = result.all()
    return rows, total


async def delete_history(db: AsyncSession, user_id: int, history_id: int):
    result = await db.execute(
        delete(History).where(History.user_id == user_id).where(History.id == history_id))
    await db.commit()
    return result.rowcount >0


async def delete_all_history(db: AsyncSession, user_id: int):
    await db.execute(delete(History).where(History.user_id == user_id))
    await db.commit()
    return True


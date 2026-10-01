
from fastapi import APIRouter, Depends, Query, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import history

from models.users import User
from schemas.history import HistoryRequest, HistoryCheckResponse, HistoryListResponse, HistoryNewsItemResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix='/api/history', tags=['history'])

@router.get("/check")
async def check_favorite(news_id:int,current_user: User = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    is_historied = await history.get_check_history(db,news_id,user_id=current_user.id)
    return success_response(
        message="收藏检查成功",
        data=HistoryCheckResponse(isHistory=is_historied)
    )

@router.post("/add")
async def add_history(req:HistoryRequest,user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    data =await history.add_history(db,user.id,req.newsId)
    return success_response(
        message="添加成功",
        data=data
    )

@router.get("/list")
async def get_history(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
        page:int = Query(1,alias="page"),
        page_size:int = Query(10,le=100,alias="pageSize")):
    rows,total = await history.get_history_list(db,user.id,page,page_size)
    history_list=[HistoryNewsItemResponse(
        id =history_id,
        newsId=news. id  ,
        title=news.title,
        image=news.image,
        author=news.author,
        views=news.views,
        publishTime=news.publish_time,
        viewTime=history_time
        )for news,history_time,history_id in rows]
    has_more = total > page * page_size
    data = HistoryListResponse(list=history_list,total=total,hasMore=has_more)
    return success_response(
        message="获取成功",
        data=data
    )

@router.delete("/delete/{history_id}")
async def delete_history(
        history_id:int,
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)
):
    result = await history.delete_history(db,user.id,history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="记录不存在")
    return success_response(
        message="删除成功"
    )
@router.delete("/clear")
async def clear_history(
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    await history.delete_all_history(db,user.id)
    return success_response(
        message="清空成功"
    )





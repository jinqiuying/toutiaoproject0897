from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db

from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def check_favorite(
        news_id:int = Query(...,alias="newsId"),
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)

):
    is_favorited = await favorite.get_check_favorite(news_id, user.id, db)
    return success_response(
        message="收藏检查成功",
        data=FavoriteCheckResponse(isFavorite=is_favorited)
    )

@router.post("/add")
async def add_favorite(
        data:FavoriteAddRequest,
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)
):
    new_favorite = await favorite.add_news_favorite(data.news_id, user.id, db)
    return success_response(
        message="收藏成功",
        data=new_favorite
    )

@router.delete("/remove")
async def remove_favorite(
        news_id:int = Query(...,alias="newsId"),
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)
):
    result =await favorite.remove_favorite(news_id, user.id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="收藏记录不存在")
    return success_response(
        message="取消收藏成功"
        # data=FavoriteRemoveRequest(newsId = news_id)
    )


@router.get("/list")
async def list_favorite(
        user:User=Depends(get_current_user),
        page:int=Query(1,alias="page"),
        page_size:int=Query(10,alias="pageSize"),
        db:AsyncSession = Depends(get_db)
):
    rows,total =await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list =[{
        **news.__dict__,
        "favoriteTime":favorite_time,
        "favoriteId":favorite_id
    }for news,favorite_time,favorite_id in rows]
    has_more = total > page * page_size
    data = FavoriteListResponse(list=favorite_list, total=total, hasMore=has_more)

    return success_response(
        message="收藏列表获取成功",
        data=data
    )

@router.delete("/clear")
async def clear_favorite(
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)
):
    total = await favorite.clear_favorite(user.id, db)
    return success_response(
        message=f"清空{total}条收藏成功"
    )


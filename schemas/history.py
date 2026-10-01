from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class HistoryCheckResponse(BaseModel):
    isHistory: bool

class HistoryRequest(BaseModel):
    newsId: int
    model_config = ConfigDict(from_attributes=True)

class HistoryNewsItemResponse(BaseModel):
    id: int
    newsId: int
    title: str
    image: str
    author: str
    views: int
    publishTime: datetime
    viewTime: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryListResponse(BaseModel):
    list: List[HistoryNewsItemResponse]
    total: int
    hasMore: bool

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class HistoryNewsDeleteRequest(BaseModel):
    news_id: int = Field( alias="newsId")
    model_config = ConfigDict(from_attributes=True)
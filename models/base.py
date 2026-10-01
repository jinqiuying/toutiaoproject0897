from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field, BaseModel


class NewsItemBase(BaseModel):
    id:int
    title:str
    content: Optional[str] = None  # ← 加上这一行
    description:Optional[str]=None
    image:Optional[str]=None
    author:Optional[str]=None
    category_id:int=Field(alias="categoryId")
    views:int
    publish_time:Optional[datetime]=Field(None,alias="publishTime")
    model_config = ConfigDict(
        populate_by_name = True,
        from_attributes = True
    )
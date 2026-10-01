from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, Index
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

#定义新闻分类的模型类

#创建基类+表对应的模型类
class Base(DeclarativeBase):
    created_at :Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment = "创建时间")
    updated_at :Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment = "更新时间")




#创建模型类
class NewsCategory(Base):
    __tablename__ = 'news_category'
    id :Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name :Mapped[str] = mapped_column(String(50), unique = True,comment="分类名称")
    sort_order :Mapped[int] = mapped_column(Integer,default = 0, nullable=False, comment="排序顺序")
    #打印对象
    def __repr__(self):
        return f"<NewsCategory(id={self.id}, name={self.name}, sort_order={self.sort_order})>"




class NewsList(Base):
    __tablename__ = 'news'
    #创建索引提升查询速度
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),
        Index('idx_publish_time_idx', 'publish_time')
    )
    id :Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title :Mapped[str] = mapped_column(String(255), comment="新闻标题")
    description :Mapped[Optional[str]] = mapped_column(String(500), comment="新闻描述")
    content :Mapped[str] = mapped_column(Text, comment="新闻内容")
    image :Mapped[Optional[str]] = mapped_column(String(255), comment="新闻图片")
    author :Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id :Mapped[int] = mapped_column(Integer, comment="分类ID")
    views :Mapped[int] = mapped_column(Integer, default=0, comment="浏览次数")
    publish_time :Mapped[datetime] = mapped_column(DateTime, comment="发布时间")

    def __repr__(self):
        return f"<NewsList(id= {self. id } , title= {self.title} , author= {self.author} , category_id= {self.category_id} )>"



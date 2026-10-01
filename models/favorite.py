from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    __tablename__ = "favorite"
    __table_args__ = (
        #唯一约束，当前新闻只能收藏一次
        UniqueConstraint("user_id", "news_id", name="user_news_unique"),
        Index("idx_user_id", "user_id"),
        Index("idx_news_id", "news_id"),
    )
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="收藏ID")
    user_id:Mapped[int] = mapped_column(Integer,comment="用户ID")
    news_id:Mapped[int] = mapped_column(Integer,comment="新闻ID")
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment="收藏时间")


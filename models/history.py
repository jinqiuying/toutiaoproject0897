from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    pass

class History(Base):
    __tablename__ = "history"
    __table_args__ = (
        UniqueConstraint('user_id','news_id'),
        Index('idx_user_id','user_id'),
        Index('idx_news_id','news_id'),
    )
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer,comment='用户ID')
    news_id:Mapped[int] = mapped_column(Integer,comment='新闻ID')
    view_time:Mapped[datetime] = mapped_column(DateTime,default=datetime.now(),comment='浏览时间')
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Index, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass




class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        Index('username_UNIQUE','username',unique=True),
        Index('phone_UNIQUE','phone')
    )
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username:Mapped[str] = mapped_column(String(50), unique = True,comment="用户名")
    password:Mapped[str] = mapped_column(String(255), unique = True,comment="密码")
    nickname:Mapped[str] = mapped_column(String(50), comment="昵称")
    avatar:Mapped[Optional[str]] = mapped_column(String(255), comment="头像",default="/image/default.jpg")
    gender:Mapped[Optional[str]] = mapped_column(String(10), comment="性别")
    bio:Mapped[Optional[str]] = mapped_column(String(255), comment="个人简介",default="这个人很懒，没有留下签名")
    phone:Mapped[Optional[str]] = mapped_column(String(255), comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<UserRegister(username={self.username}, password={self.password}, nickname={self.nickname}, avatar={self.avatar}, gender={self.gender}, bio={self.bio}, phone={self.phone})>"

class UserToken(Base):
    __tablename__ = "user_token"
    __table_args__ = (
        Index('idx_user_id','user_id',unique=True),
    )
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    token:Mapped[str] = mapped_column(String(255), comment="令牌")
    created_at :Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment = "创建时间")
    expires_at :Mapped[datetime] = mapped_column(DateTime,default=datetime.now,comment = "过期时间")


    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token={self.token})>"

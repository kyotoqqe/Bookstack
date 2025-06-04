import enum
from datetime import datetime
from uuid import UUID

from sqlalchemy import String, BigInteger, Enum as SQLEnum, Uuid, ForeignKey, func
from sqlalchemy.orm import Mapped,mapped_column, relationship

from src.database.base import Base

class Role(enum.Enum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"
    moderator = "moderator"
    banned = "banned"


class Users(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(50), unique=True)
    email:Mapped[str] = mapped_column(String(128), unique=True)
    password:Mapped[str] = mapped_column(String(60))
    """ role:Mapped[str] = mapped_column(
                        SQLEnum(enums=Role, name="user_roles"),
                        default=Role.user
                        ) """
    active:Mapped[bool] = mapped_column(default=False)

    refresh_sessions:Mapped[list["RefreshSessions"]] = relationship(
        back_populates="user"
    )

class RefreshSessions(Base):
    __tablename__ = "refresh_sessions"
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    refresh_token:Mapped[UUID] #maybe string
    #user_agent:Mapped[str] = mapped_column(String(200)) 
    #fingerprint:Mapped[str] = mapped_column(String(200))
    #ip:Mapped[str] = mapped_column(String(15))
    expires_in:Mapped[int] = mapped_column(BigInteger)
    created_at:Mapped[datetime] = mapped_column(server_default=func.now())

    user:Mapped["Users"] = relationship(
        back_populates="refresh_sessions"
    ) 
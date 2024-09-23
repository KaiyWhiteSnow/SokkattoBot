from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from .user_model import User
from .. import Base

class Bot(Base):
    __tablename__ = 'Bot'

    bot_id = Column(
        Integer, 
        nullable=False, 
        primary_key=True, 
        autoincrement=True
    )
    bot_to_user_id = Column(
        Integer, 
        ForeignKey(User.user_id),
        nullable=False
    )
    name = Column(
        String, 
        nullable=False,
    )
    ip = Column(
        String, 
        nullable = False
    )
    port = Column(
        String, 
        nullable = False
    )
    token = Column(
        Integer, 
        nullable = False
    )
    steam_id = Column(
        Integer, 
        nullable = True
    )
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from .bot_model import Bot
from .. import Base

class Switch(Base):
    __tablename__ = 'Switch'
    
    switch_id = Column(        
        Integer, 
        nullable=False, 
        primary_key=True, 
        autoincrement=True
    )
    switch_to_bot_id = Column(
        Integer, 
        ForeignKey(Bot.bot_id),
        nullable=False
    )
    switch_name = Column(
        String,
        nullable=False
    )
    switch_key = Column(
        Integer,
        nullable=False,
    )
    
from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from Database.UserModel import Users

Base = declarative_base()

class Bots(Base):
    __tablename__ = 'Bots'

    BotID = Column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )
    
    Id = Column(
        Integer, 
        ForeignKey(Users.User_ID),
        nullable=False
    )
    Name = Column(
        String, 
        nullable=False,
    )
    Ip = Column(
        String, 
        nullable = False
    )
    Port = Column(
        String, 
        nullable = False
    )
    Token = Column(
        Integer, 
        nullable = False
    )
    SteamID = Column(
        Integer, 
        nullable = True
    )

from sqlalchemy import Column, Integer, String
from .. import Base

class User(Base):
    __tablename__ = "User"

    user_id = Column(
        Integer, 
        nullable=False, 
        unique=True, 
        primary_key=True, 
        autoincrement=True
    )
    username = Column(
        String, 
        nullable=False
    )
    password = Column(
        String, 
        nullable=False
    )
    description = Column(
        String, 
        nullable=True
    )
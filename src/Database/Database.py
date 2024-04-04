from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.state import InstanceState

engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

from Database.UserModel import Base as UserBase
UserBase.metadata.create_all(engine)
from Database.BotModel import Base as BotBase
BotBase.metadata.create_all(engine)
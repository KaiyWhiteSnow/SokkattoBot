from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.state import InstanceState
from sqlalchemy.ext.declarative import declarative_base

from .models import user_model

Base = declarative_base()

engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
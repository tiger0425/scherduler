# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tasks.settings import USER_MYSQL_CONNSTR
from datetime import datetime

# declare a Mapping,this is the class describe map to table column
Base = declarative_base()


class User(Base):
    username = Column(String(50), default='')
    email = Column(String(50), default='')
    password = Column(String(50))
    host = Column(String(50), default='www.amazon.com')
    proxy = Column(String(50), default='')
    nickname = Column(String(50), default='')
    address = Column(String(255), default='')
    zip = Column(String(50), default='')
    state = Column(String(50), default='')
    city = Column(String(50), default='')
    used = Column(String(20), default='')
    created = Column(DateTime, nullable=False, default=datetime.now())


def create_session():
    # declare the connecting to the server
    engine = create_engine(USER_MYSQL_CONNSTR, echo=False)
    # connect session to active the action
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

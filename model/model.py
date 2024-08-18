from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserActivity(Base):
    __tablename__ = 'activity_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    controller_name = Column(String)
    action_type_id = Column(Integer)
    action = Column(String)
    request_params = Column(String)
    response = Column(String)
    timestamp = Column(DateTime)

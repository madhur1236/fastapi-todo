from click import DateTime
from sqlalchemy import Column, Integer, String, Boolean, DateTime,func
from database import Base

class ToDo(Base):
    __tablename__ = 'todos'

    id = Column(Integer,primary_key=True, index = True)
    title = Column(String,index=True)
    description = Column(String, nullable= True)
    completed = Column(Boolean, default = False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
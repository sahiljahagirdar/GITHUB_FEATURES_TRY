from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import relationship
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = 'Users'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    username = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
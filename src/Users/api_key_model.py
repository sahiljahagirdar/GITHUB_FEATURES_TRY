from sqlalchemy import (Column,String,ForeignKey,DateTime,Integer,Boolean)
from sqlalchemy.sql import func
from src.utils.db import Base

class APIKEY(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String,nullable=False,unique=True)
    user_id = Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"))
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    last_used = Column(DateTime(timezone=True),nullable=True)
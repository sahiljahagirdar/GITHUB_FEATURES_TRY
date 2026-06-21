from sqlalchemy import Column, Integer, String, Text, Date
from src.utils.db import Base

class Episode(Base):
    __tablename__ = "TMKOC_episodes"

    id = Column(Integer, primary_key=True, index=True)
    episode_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    runtime = Column(Integer)
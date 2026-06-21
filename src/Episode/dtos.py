from pydantic import BaseModel
from typing import List

class ResponseModel(BaseModel):
    episode_number:int
    title : str
    description : str
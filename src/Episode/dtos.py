from pydantic import BaseModel
from typing import List

class ResponseModel(BaseModel):
    episode_number:int
    title : str
    description : str

class PaginatedEpisodeResponse(BaseModel):
    page: int
    limit: int
    total_records: int
    total_pages: int
    has_next: bool
    has_previous: bool
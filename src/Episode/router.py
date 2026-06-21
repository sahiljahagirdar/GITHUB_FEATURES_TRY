from fastapi import APIRouter, Depends, Query, Request
from src.Episode.dtos import ResponseModel,PaginatedEpisodeResponse
from src.utils.db import get_db
from src.Episode import controller
from src.utils.helpers import is_authenticated
from src.Users.models import UserModel
from src.utils.api_key_auth import validate_api_key
from sqlalchemy.orm import session

episode_route = APIRouter(prefix='/TMKOC',dependencies=[Depends(validate_api_key)])

@episode_route.get('/episodes',)
def all_episodes(page: int = Query(1, ge=1),limit: int = Query(20, ge=1, le=100),db: session = Depends(get_db)):
    return controller.get_episodes(page, limit, db)

@episode_route.get('/episode/{episode_id}',response_model=ResponseModel)
def one_episode(episode_id:int,db:session = Depends(get_db)):
    return controller.get_one_episode(episode_id,db)

@episode_route.get('/status')
def my_status(db:session = Depends(get_db)):
    return controller.stats(db)

@episode_route.get('/random',response_model=ResponseModel)
def get_random_episode(db = Depends(get_db)):
    return controller.generate_random_episode(db)

@episode_route.get('/latest_episode',response_model=ResponseModel)
def latest_episode(db=Depends(get_db)):
    return controller.latest_episode(db)

@episode_route.get('/search',response_model=PaginatedEpisodeResponse)
def search_episodes(keyword: str,page: int = Query(1, ge=1),limit: int = Query(20, ge=1, le=100),db: session = Depends(get_db)):
    return controller.search_episodes(keyword, page, limit, db)
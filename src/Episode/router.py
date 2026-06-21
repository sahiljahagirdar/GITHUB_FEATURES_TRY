from fastapi import APIRouter, Depends, Query, Request
from src.Episode.dtos import ResponseModel,PaginatedEpisodeResponse
from src.utils.db import get_db
from src.Episode import controller
from src.utils.helpers import is_authenticated
from src.Users.models import UserModel
from src.utils.api_key_auth import validate_api_key
from src.utils.limiter import limiter
from sqlalchemy.orm import session

episode_route = APIRouter(prefix='/TMKOC',dependencies=[Depends(validate_api_key)])

@episode_route.get('/episodes')
@limiter.limit('10000/minute')
def all_episodes(request:Request,page: int = Query(1, ge=1),limit: int = Query(20, ge=1, le=100),db: session = Depends(get_db)):
    return controller.get_episodes(page, limit, db)

@episode_route.get('/episode/{episode_id}',response_model=ResponseModel)
@limiter.limit("10000/minute")
def one_episode(request:Request,episode_id:int,db:session = Depends(get_db)):
    return controller.get_one_episode(episode_id,db)

@episode_route.get('/status')
@limiter.limit("1000/minute")
def my_status(request:Request,db:session = Depends(get_db)):
    return controller.stats(db)

@episode_route.get('/random',response_model=ResponseModel)
@limiter.limit("3000/minute")
def get_random_episode(request:Request,db = Depends(get_db)):
    return controller.generate_random_episode(db)

@episode_route.get('/latest_episode',response_model=ResponseModel)
@limiter.limit("6000/minute")
def latest_episode(request:Request,db=Depends(get_db)):
    return controller.latest_episode(db)

@episode_route.get('/search',response_model=PaginatedEpisodeResponse)
@limiter.limit("2000/minute")
def search_episodes(request:Request,keyword: str,page: int = Query(1, ge=1),limit: int = Query(20, ge=1, le=100),db: session = Depends(get_db)):
    return controller.search_episodes(keyword, page, limit, db)
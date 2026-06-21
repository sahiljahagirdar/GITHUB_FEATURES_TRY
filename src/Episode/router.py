from fastapi import APIRouter, Depends, Query
from src.Users.dtos import Response_Model
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
from src.Episode.dtos import ResponseModel
from sqlalchemy.orm import session
from src.Episode.models import Episode
from src.Users.models import UserModel
from src.Episode.models import Episode
from fastapi import HTTPException, status
from sqlalchemy import func, cast, Integer,extract
from sqlalchemy import func
from math import ceil

def get_episodes(page: int, limit: int, db: session):

    total_records = db.query(func.count(Episode.id)).scalar()

    total_pages = ceil(total_records / limit)

    offset = (page - 1) * limit

    episodes = (
        db.query(Episode)
        .order_by(Episode.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    if page > total_pages:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f'Page {page} does not exists. Last available page is {total_pages}'
        )

    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "data": episodes
    }


def get_one_episode(episode_id:int,db:session):
    
    episode = db.query(Episode).filter(Episode.episode_number == str(episode_id)).first()

    if not episode:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail='episode not found'
        )
    
    return episode

def stats(db: session):

    total_episodes = db.query(func.count(Episode.id)).scalar()
    highest_episode_number = db.query(func.max(cast(Episode.episode_number, Integer))).scalar()
    first_episode = (db.query(Episode).order_by(Episode.id.asc()).first())
    last_episode = (db.query(Episode).order_by(Episode.id.desc()).first())

    missing_episodes = (highest_episode_number - total_episodes if highest_episode_number is not None else 0)

    return {
        "episodes_in_db": total_episodes,
        "highest_episode_number": highest_episode_number,
        "missing_episodes": missing_episodes,

        "first_episode": {
            "episode_number": first_episode.episode_number,
            "title": first_episode.title,
            "description": first_episode.description,
            "runtime": first_episode.runtime
        } if first_episode else None,

        "last_episode": {
            "episode_number": last_episode.episode_number,
            "title": last_episode.title,
            "description": last_episode.description,
            "runtime": last_episode.runtime
        } if last_episode else None,
    }

def generate_random_episode(db:session):
    episode = db.query(Episode).order_by(func.random()).first()

    if not episode:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Episode not found'
        )
    
    return episode
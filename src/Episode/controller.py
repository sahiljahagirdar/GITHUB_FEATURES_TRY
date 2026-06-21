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


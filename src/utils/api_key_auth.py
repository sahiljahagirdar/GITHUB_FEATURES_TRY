from fastapi import HTTPException, status, Depends, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import session
from src.utils.db import get_db
from src.Users.api_key_model import APIKEY
from datetime import datetime
import hashlib


api_key_header = APIKeyHeader(
    name="X-API-KEY",
    auto_error=False
)

def validate_api_key(api_key: str = Security(api_key_header),db: session = Depends(get_db)):
    
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="No API key provided"
        )
    
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    key = (db.query(APIKEY).filter(APIKEY.key_hash == key_hash,APIKEY.is_active == True).first())

    if not key:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid API key'
        )
    
    key.last_used = datetime.now()

    db.commit()
    
    return key
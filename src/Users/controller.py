from src.Users.dtos import User_Schema,Login_Schema
from sqlalchemy.orm import session
from src.Users.models import UserModel
from fastapi import HTTPException,status
from src.utils.settings import settings
from datetime import datetime,timedelta
from src.utils.api_key import generate_api_key
from src.Users.api_key_model import APIKEY
from pwdlib import PasswordHash
import jwt

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)



def register_user(body: User_Schema, db: session):

    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()

    if is_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username Already Exists"
        )
    
    if is_email:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Email Already exists'
        )
    
    hashed_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username = body.username,
        email=body.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(body:Login_Schema,db:session):
    is_user = (db.query(UserModel).filter(UserModel.username == body.username).first())

    if not is_user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    if not verify_password(body.password, is_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Check email or password"
        )

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode(
        {
            "_id": is_user.id,
            "exp": exp_time.timestamp()
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {"token": token}

def my_profile(db:session,user:UserModel):
    user = db.query(UserModel).filter(UserModel.username == user.username).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail='User Not Found'
        )
    
    return user

def generate_API_key(db:session,user:UserModel):
    
    raw_key, key_hash = generate_api_key()

    api_key = APIKEY(
        key_hash = key_hash,
        user_id = user.id
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "api_key" : raw_key
    }
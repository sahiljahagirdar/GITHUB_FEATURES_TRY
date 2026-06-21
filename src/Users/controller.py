from src.Users.dtos import User_Schema
from sqlalchemy.orm import session
from src.Users.models import UserModel
from fastapi import HTTPException,status
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)



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
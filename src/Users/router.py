from fastapi import APIRouter,Depends,status,Request
from src.utils.db import get_db
from src.Users.models import UserModel
from src.Users.dtos import User_Schema,Response_Model,Login_Schema,UserResponseProfile
from src.Users import controller
from src.utils.helpers import is_authenticated
from src.utils.limiter import limiter
from typing import List

User_route = APIRouter(prefix='/Auth')


@User_route.post('/register',response_model=Response_Model)
@limiter.limit("300/minute")
def create_account(request: Request,body:User_Schema,db = Depends(get_db)):
    return controller.register_user(body,db)


@User_route.post('/login')
@limiter.limit("500/minute")
def login(request: Request,body: Login_Schema,db=Depends(get_db)):
    return controller.login_user(body, db)

@User_route.get('/profile',response_model=UserResponseProfile)
def get_me(db = Depends(get_db),user:UserModel = Depends(is_authenticated)):
    return controller.my_profile(db,user)

@User_route.post('/get_api_key')
def generate_api_key(db=Depends(get_db),user:UserModel = Depends(is_authenticated)):
    return controller.generate_API_key(db,user)

@User_route.get('/my_api_keys')
def get_my_keys(db=Depends(get_db),user:UserModel = Depends(is_authenticated)):
    return controller.get_my_api_key(db,user)

@User_route.delete('/delete_api_key/{api_key_id}')
def delete_api_key(api_key_id:int,db = Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.delete_api_key(api_key_id,db,user)
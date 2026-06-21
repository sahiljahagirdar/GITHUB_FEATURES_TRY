from fastapi import APIRouter,Depends,status
from src.utils.db import get_db
from src.Users.models import UserModel
from src.Users.dtos import User_Schema,Response_Model,Login_Schema,UserResponseProfile
from src.Users import controller
from src.utils.helpers import is_authenticated
from typing import List

User_route = APIRouter(prefix='/Auth')


@User_route.post('/register',response_model=Response_Model)
def create_account(body:User_Schema,db = Depends(get_db)):
    return controller.register_user(body,db)

@User_route.post('/login')
def login(body:Login_Schema,db = Depends(get_db)):
    return controller.login_user(body,db)

@User_route.get('/profile',response_model=UserResponseProfile)
def get_me(db = Depends(get_db),user:UserModel = Depends(is_authenticated)):
    return controller.my_profile(db,user)
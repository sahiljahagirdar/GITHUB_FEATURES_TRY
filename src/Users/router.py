from fastapi import APIRouter,Depends,status
from src.utils.db import get_db
from src.Users.models import UserModel
from src.Users.dtos import User_Schema,Response_Model
from src.Users import controller
from typing import List

User_route = APIRouter(prefix='/Auth')


@User_route.post('/register',response_model=Response_Model)
def create_account(body:User_Schema,db = Depends(get_db)):
    return controller.register_user(body,db)
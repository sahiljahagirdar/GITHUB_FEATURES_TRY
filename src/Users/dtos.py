from pydantic import BaseModel,EmailStr,field_validator,Field
from datetime import datetime

class User_Schema(BaseModel):
    name : str = Field(...,min_length=5)
    username : str = Field(...,min_length=5)
    email : EmailStr
    password : str = Field(...,min_length=5)

    @field_validator("name","username","password")
    @classmethod
    def validate_fields(cls,value):
        if not value.strip():
            raise ValueError("Field cannot be empty")
        return value
    
class Login_Schema(BaseModel):
    username : str
    password : str

    @field_validator("username","password")
    @classmethod
    def validate_fields(cls,value):
        if not value.strip():
            raise ValueError('Field cannot be empty')
        return value
    

class Response_Model(BaseModel):
    username : str
    email : str

class UserResponseProfile(BaseModel):
    id : int
    name : str
    username : str
    email : str
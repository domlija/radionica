from fastapi import APIRouter, Cookie, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..db.models import User, BlogPost
from typing import Annotated

class UserPy(BaseModel):
    username : str 
    password : str

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get('/{username}')
async def get_user(username):
    user = User.fetch_by_username(username)
    print(user)
    posts = BlogPost.fetch_by_creator_id(user.id)
    user.posts = posts

    return {
        user
    }

@router.put('/')
async def create_user(user: UserPy):
    User.insert_user(user.username, user.password)
    return user

@router.post('/login')
async def login_user(username: Annotated[str, Form()], password:Annotated[str, Form()]):
    user_id = User.login_user(username, password)
    if user_id == None:
        return JSONResponse({"message": "failure"})
    
    res = JSONResponse({"message": "success"})
    res.set_cookie(key="user_id", value=str(user_id), secure=True, httponly=True)
    return res
    
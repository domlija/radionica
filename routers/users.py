from fastapi import APIRouter, Cookie, Form, Request
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from db.models import User, BlogPost
from typing import Annotated
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

class UserPy(BaseModel):
    username : str 
    password : str

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.get('/login')
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.view.html", context={"request": request})   

@router.get('/logout')
async def logout_user(req: Request):
    res = RedirectResponse('/', status_code=302)
    res.delete_cookie(key='user_id')
    return res

@router.get('/{username}')
async def get_user(username, req: Request):
    try:
        user = User.fetch_by_username(username)
        print(user)
        posts = BlogPost.fetch_by_creator_id(user.id)
        user.posts = posts
        print(posts)


        user_logged = False 
        same_user_logged = False
        if req.cookies.get('user_id') == user.id:
            same_user_logged = True
            user_logged = True

        if req.cookies.get('user_id'):
            user_logged = True


        return templates.TemplateResponse('user.view.html', context={
            "request": req,
            "data": user,
            "logged": user_logged,
            "owner_logged": same_user_logged
        })

        return {
            user
        }
    except Exception as e:
        

       return {"message": e}

@router.put('/')
async def create_user(user: UserPy):
    User.insert_user(user.username, user.password)
    return user

@router.post('/login')
async def login_user(username: Annotated[str, Form()], password:Annotated[str, Form()]):
    user_id = User.login_user(username, password)
    if user_id == None:
        return JSONResponse({"message": "failure"})
    
    res = RedirectResponse('/users/' + username, status_code=302)
    res.set_cookie(key="user_id", value=str(user_id), secure=True, httponly=True)
    return res

@router.get('/logout')
async def logout_user(req: Request):
    res = RedirectResponse('/', status_code=302)
    res.delete_cookie(key='user_id')
    return res

 
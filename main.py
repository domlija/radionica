from typing import Annotated
from fastapi import Depends, FastAPI, Form, Request
from db.models import User
from routers import users, posts, comments
from fastapi.responses import JSONResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/")
async def root(req: Request):
    

@app.get("/search")
async def search_user(username: str = ''):
    


@app.get('/signup')
async def get_signup_page(request: Request):
    

@app.post('/signup')
async def signup_user(username: Annotated[str, Form()], password: Annotated[str, Form()], passwordRepeat: Annotated[str, Form()]):


@app.get('/login')
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.view.html", context={"request": request})   


@app.post('/login')
async def login_user(username: Annotated[str, Form()], password:Annotated[str, Form()]):


@app.get('/logout')
async def logout_user(req: Request):
    res = RedirectResponse('/', status_code=302)
    res.delete_cookie(key='user_id')
    return res



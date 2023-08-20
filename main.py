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
    user_logged = False
    if req.cookies.get('user_id'):
        user_logged = True 


    return templates.TemplateResponse('landing.view.html', {"request": req, "logged": user_logged})

@app.get("/search")
async def search_user(username: str = ''):
    print(username)
    if username == '':
        return RedirectResponse("/")
    return RedirectResponse("/users/" + username, status_code=302)


@app.get('/signup')
async def get_signup_page(request: Request):
    logged = True if request.cookies.get('user_id') else False 
    return templates.TemplateResponse("signup.view.html", context={"request": request, "logged": logged})

@app.post('/signup')
async def signup_user(username: Annotated[str, Form()], password: Annotated[str, Form()], passwordRepeat: Annotated[str, Form()]):
    try:    
        User.fetch_by_username(username)
        return {"status": "username exists"}
    except:
        User.insert_user(username, password)
        return {"status": "Sign up successful"}

@app.get('/login')
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.view.html", context={"request": request})   


@app.post('/login')
async def login_user(username: Annotated[str, Form()], password:Annotated[str, Form()]):
    user_id = User.login_user(username, password)
    if user_id == None:
        return JSONResponse({"message": "failure"})
    
    res = RedirectResponse('/users/' + username, status_code=302)
    res.set_cookie(key="user_id", value=str(user_id), secure=True, httponly=True)
    return res

@app.get('/logout')
async def logout_user(req: Request):
    res = RedirectResponse('/', status_code=302)
    res.delete_cookie(key='user_id')
    return res



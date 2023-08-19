from fastapi import Depends, FastAPI, Request
from routers import users, posts, comments
from fastapi.responses import RedirectResponse

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



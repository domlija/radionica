from fastapi import APIRouter, Cookie, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Request
from pydantic import BaseModel
from db.models import User, BlogPost, Comment
from typing import Annotated
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get('/')
async def get_create_post(req: Request):
    logged = True if req.cookies.get('user_id') else False 

    if not logged:
        return {"status": "not logged in!"}

    return templates.TemplateResponse("createPost.view.html", context={"request": req,
                                                                       "logged": logged})

@router.get('/{post_id}')
async def get_post(post_id, request: Request):
    post = BlogPost.fetch_by_id(post_id)
    comments = Comment.fetch_by_post_id(post_id)
    logged = True if request.cookies.get('user_id') else False
    #return post
    return templates.TemplateResponse("blog.view.html", {"post_id": post_id, 
                                                         "title": post.title, 
                                                         "body": post.body, 
                                                         "request": request, 
                                                         "comments": comments,
                                                         "logged": logged})


@router.post('/')
async def put_post(title: Annotated[str, Form()], body: Annotated[str, Form()], request: Request):
    user_id = request.cookies.get("user_id")
    if user_id == None:
        return {"status": "failed"}
    
    user = User.fetch_by_id(user_id)


    BlogPost.insert_post(title, body, user_id)

    return RedirectResponse("/users/" + user.username, status_code=302)

@router.delete('/{post_id}')
async def delete_post(post_id, req: Request):
    user_id = req.cookies.get("user_id")

    if user_id == None:
        return {"status": "unauthorized"}
    
    post = BlogPost.fetch_by_id(post_id)

    if post.cretor_id == user_id:
        BlogPost.delete_post(post_id)
        return {"status": "success"}
    else:
        return {"status": "User can only delete their own posts."}


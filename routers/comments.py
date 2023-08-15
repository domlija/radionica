from fastapi import APIRouter, Cookie, Form
from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel
from ..db.models import User, BlogPost, Comment
from typing import Annotated


router = APIRouter(
    prefix="/comments",
    tags=['comments']
)

@router.put('/')
async def create_comment(post_id: Annotated[str, Form()], text: Annotated[str, Form()]):
    Comment.insert_comment(text, post_id)
    return {"status": "success"}
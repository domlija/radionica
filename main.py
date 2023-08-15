from fastapi import Depends, FastAPI
from .routers import users, posts, comments
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}



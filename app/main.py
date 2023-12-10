from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
my_posts = [
                {"title": "Title post 1", "content": "Content post 1", "id": 1},
                {"title": "Title post 2", "content": "Content post 2", "id": 2},
            ]

def find_post(id):
    for post in my_posts:
        if post["id"] == int(id):
            return post

def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Wellcome to my api"}

@app.get("/post/latest")
def get_post_latest():
    post = my_posts[len(my_posts) -1]
    return {"latest post": post}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
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
app.include_router(vote.router)
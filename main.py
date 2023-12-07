from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    pulished: bool = True
    rating: Optional[int] = None
    
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

@app.get("/post")
def get_posts():
    return {"data": my_posts}

@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/post/latest")
def get_post_latest():
    post = my_posts[len(my_posts) -1]
    return {"latest post": post}

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post_id = find_post(id)
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found!"}
    return {f"post {id}": post_id}


@app.delete("/post/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int):
    #deleting post
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found!")
    
    my_posts.pop(index)
    return {"message": f"deleted post with id {id}"}


@app.put("/post/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found!")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": f"updated post with id {id}", "data": post_dict}

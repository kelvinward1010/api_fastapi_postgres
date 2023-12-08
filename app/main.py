from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
    
#Connect with postgres database
while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='fastapi', 
                                user='postgres', 
                                password='kelvin',
                                cursor_factory=RealDictCursor
                                )
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as error:
        print("Connection failed!")
        print("Error: %s" % error)
        time.sleep(2)
    
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

@app.get("/post", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(new_post: schemas.CreatePost, db: Session = Depends(get_db)):
    # post_dict = new_post.dict()
    # post_dict["id"] = randrange(0,100000)
    # my_posts.append(post_dict)
    
    #cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({new_post.title}, {new_post.content}, {new_post.published})")
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published)
    #                )
    # new_post = cursor.fetchone()
    # conn.commit()
    
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

@app.get("/post/latest")
def get_post_latest():
    post = my_posts[len(my_posts) -1]
    return {"latest post": post}

@app.get("/post/{id}")
def get_post(id: int, response: Response,  db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts Where id = %s""", (str(id)))
    # post_find = cursor.fetchone()
    
    #post_id = find_post(id)
    
    post_find = db.query(models.Post).filter(models.Post.id == id).first()
    
    
    if not post_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found!"}
    return post_find


@app.delete("/post/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int, db: Session = Depends(get_db)):
    #deleting post
    #index = find_index_post(id)
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found!")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    #my_posts.pop(index)
    return {"message": f"deleted post with id {id}"}


@app.put("/post/{id}")
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    #index = find_index_post(id)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = post_query.first()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found!")
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
        
    return post_query.first()



#Users

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
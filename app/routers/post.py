from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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


@router.get("/{id}")
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


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
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


@router.put("/{id}")
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
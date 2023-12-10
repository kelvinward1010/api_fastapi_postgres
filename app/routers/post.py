from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    #return data all
    posts = db.query(models.Post).all()
    
    return posts

@router.get("/posts_user_token", response_model=List[schemas.Post])
def get_posts_user_token(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #return data follow owner_id (User)    
    post_query_follow_user = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    return post_query_follow_user

@router.get("/search", response_model=List[schemas.Post])
def search_posts(db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user),
                 limit: int = 10,
                 skip: int = 0,
                 search: Optional[str] = ""
                ):
    
    #return data all
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.get("/posts_vote", response_model=List[schemas.PostOutVote])
def get_posts_vote(db: Session = Depends(get_db), 
                   current_user: int = Depends(oauth2.get_current_user),
                   search: Optional[str] = ""):
    
    #return data all post with votes
    posts_vote_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).all()
    
    posts = []
    for post in posts_vote_query:
        posts.append(post._asdict())
    
    return posts

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post_dict = new_post.dict()
    # post_dict["id"] = randrange(0,100000)
    # my_posts.append(post_dict)
    
    #cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({new_post.title}, {new_post.content}, {new_post.published})")
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published)
    #                )
    # new_post = cursor.fetchone()
    # conn.commit()
     
    post = models.Post(owner_id = current_user.id, **new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post


@router.get("/{id}",  response_model=schemas.Post)
def get_post(id: int, response: Response,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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

@router.get("/post_vote/{id}",  response_model=schemas.PostOutVote)
def get_one_post_vote(id: int, response: Response,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_find = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
    return post_find


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #deleting post
    #index = find_index_post(id)
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to delete!"
                            )
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    #my_posts.pop(index)
    return {"message": f"deleted post with id {id}"}


@router.put("/{id}",  response_model=schemas.Post)
def update_post(id: int, post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    #index = find_index_post(id)
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = post_query.first()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {id} not found!")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to updated!"
                            )
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
        
    return post_query.first()
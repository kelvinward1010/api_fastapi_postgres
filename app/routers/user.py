from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import engine, get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


#Users
@router.get("/", response_model=List[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    
    users = db.query(models.User).all()
    return users

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #has the password 
    hashed_password = utils.has_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user_find = db.query(models.User).filter(models.User.id == id).first()
    
    if not user_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {id} not found!")
    return user_find


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_user(id: int, db: Session = Depends(get_db)):
    
    deleted_user = db.query(models.User).filter(models.User.id == id)
    
    if deleted_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found!")
    
    deleted_user.delete(synchronize_session=False)
    db.commit()
    
    return {"message": f"Deleted user with id: {id}"}


@router.put("/{id}")
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.id == id)
    updated_user = user_query.first()
    
    if updated_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found!")
    
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
        
    return user_query.first()
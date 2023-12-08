from pydantic import BaseModel, EmailStr
from datetime import datetime



#Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    
class CreatePost(PostBase):
    pass
    
class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool
    
        
        
#Users
class UserBase(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: EmailStr
    password: str
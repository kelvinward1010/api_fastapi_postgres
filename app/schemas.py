from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



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
        from_attributes = True
    
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
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    


#Token
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
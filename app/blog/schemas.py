from pydantic import BaseModel
from typing import List
from typing import Optional

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        arbitrary_types_allowed = True

class User(BaseModel):
    name: str
    email: str
    password: str

# Response Model
class ShowUsermodel(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    class Config(): # required to pass because we call orm at function
        arbitrary_types_allowed = True

# Response Model
class ShowBlogModel(BaseModel):
    title: str
    body: str
    creator: ShowUsermodel
    class Config(): # required to pass because we call orm at function
        arbitrary_types_allowed = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    id: Optional[int] = None
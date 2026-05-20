from pydantic import BaseModel

# Auth Schemas
class CreateUser(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class LoginUser(BaseModel):
    username: str
    password: str

# Post Schemas
class CreatePost(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        from_attributes = True
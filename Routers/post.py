from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session 
from database import get_db
from Routers.auth import verify_token
import Models 
import Schemas



router = APIRouter()


@router.post("/posts")
def create_post(token : str, post : Schemas.CreatePost,db : Session = Depends(get_db)):
    
    user_id = verify_token(token)
    new_post = Models.Post(title = post.title , content = post.content,owner_id = user_id)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts")
def get_posts( db : Session = Depends(get_db)):
    posts = db.query(Models.Post).all()
    return posts




@router.get("/posts/{post_id}")
def get_post(post_id : int ,db : Session = Depends(get_db)):
    post = db.query(Models.Post).filter(Models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail="post not found!")
    
    return post




@router.put("/posts/{post_id}")
def update_post(token: str, post_id: int, new_post: Schemas.CreatePost, db: Session = Depends(get_db)):
    user_id = verify_token(token)
    
    post = db.query(Models.Post).filter(Models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found!")
    
    if post.owner_id != user_id:
        raise HTTPException(status_code=403, detail="this is not your post!")
    
    post.title = new_post.title
    post.content = new_post.content
    db.commit()
    
    return {"message": "Post updated!"}


@router.delete("/posts/{post_id}")
def delete_post(token: str, post_id: int, db: Session = Depends(get_db)):
    user_id = verify_token(token)        
    
    post = db.query(Models.Post).filter(Models.Post.id == post_id).first()  
    
    if not post:                          
        raise HTTPException(status_code=404, detail="Post not found!")
    
    if post.owner_id != user_id:         
        raise HTTPException(status_code=403, detail="Ye tera post nahi hai!")
    
    db.delete(post)                       
    db.commit()
    return {"message": "Post deleted!"}


    

    
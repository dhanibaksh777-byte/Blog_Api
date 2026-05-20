from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database import get_db
from datetime import datetime, timedelta
import bcrypt
import Models
import Schemas

Secrete_key = "hello123"
Access_token_Expire = 30
ALGORITHIM = "HS256"

def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def create_token(data: dict):
    Expire = datetime.utcnow() + timedelta(minutes=Access_token_Expire)
    data["exp"] = Expire
    token = jwt.encode(data, Secrete_key, algorithm=ALGORITHIM)
    return token

router = APIRouter()

@router.post("/Register", response_model=Schemas.UserResponse)
def Register(user: Schemas.CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(Models.User).filter(Models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists!")
    
    hashed_password = hash_password(user.password)
    new_user = Models.User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/Login")
def Login(user: Schemas.LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(Models.User).filter(Models.User.username == user.username).first()
    if not db_user:
        return {"error": "user not found!"}
    
    password_check = bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8"))
    if not password_check:
        return {"error": "password not correct!"}
    
    token = create_token({"user_id": db_user.id})
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, Secrete_key, algorithms=[ALGORITHIM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")

@router.get("/profile")
def profile(token: str, db: Session = Depends(get_db)):
    user_id = verify_token(token)
    user = db.query(Models.User).filter(Models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found!")
    return {"user_id": user.id, "username": user.username}

@router.put("/update_username")
def update(token: str, new_username: str, db: Session = Depends(get_db)):
    user_id = verify_token(token)
    user = db.query(Models.User).filter(Models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found!")
    user.username = new_username
    db.commit()
    return {"message": "username updated successfully!"}
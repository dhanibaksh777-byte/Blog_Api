from fastapi import FastAPI
from database import engine
import Models
from Routers import auth,post
from fastapi.middleware.cors import CORSMiddleware



Models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)




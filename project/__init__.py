from fastapi import FastAPI, APIRouter
from project.database import User, Movie, UserReview
from project.database import database as con

from .routers import users_router, reviews_router

app = FastAPI()

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(users_router)
api_v1.include_router(reviews_router)

app.include_router(api_v1)

@app.on_event('startup')
def startup():
    if con.is_closed():
        con.connect()
        
    con.create_tables([User, Movie, UserReview])
        
@app.on_event('shutdown')
def shutdown():
    if not con.is_closed():
        con.close()
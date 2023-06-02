from fastapi import HTTPException, APIRouter, Response, Cookie
from fastapi.security import HTTPBasicCredentials
from project.database import User
from project.schemas import UserRequestModel, UserResponseModel, ReviewResponseModel
from typing import List

router = APIRouter(prefix='/users')

@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409, "El username ya esta en uso")
    
    hash_password = User.create_password(user.password)
    
    user = User.create(
        username = user.username,
        password = hash_password
    )
    
    return user

@router.post("/login", response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()
    if not user:
        raise HTTPException(404, "El usuario no existe")
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(400, "La contraseña es incorrecta")
    
    response.set_cookie(key="user_id", value=user.id)
    
    return user

@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "El usuario no existe")
    
    return [user_review for user_review in user.reviews]
    
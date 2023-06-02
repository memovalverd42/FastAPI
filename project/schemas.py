from typing import Any
from pydantic import BaseModel, validator
from pydantic.utils import GetterDict
from peewee import ModelSelect

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        
        return res
    
class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
        
# ---------- VALIDACIONES DE USER ----------------- #

class UserRequestModel(BaseModel):
    username: str
    password: str
    
    @validator("username")
    def username_validator(cls, username):
        if len(username)<3 or len(username) > 50:
            raise ValueError("La longitud debe de etar entre 3 y 50 caracteres")
        
        return username
    
class UserResponseModel(ResponseModel):
    id: int
    username: str
    
# ---------- VALIDACIONES DE MOVIES ----------------- #
    
class MovieResponseModel(ResponseModel):
    id: int
    title: str
    year: int
    director: str
        
# ---------- VALIDACIONES DE REVIEW ----------------- #

class ReviewValidator():
    
    @validator("score")
    def score_validator(cls, score):
        if score < 1 or score > 10:
            raise ValueError("El score debe de estar entre 1 y 10")
        
        return score
        
class ReviewRequestModel(BaseModel, ReviewValidator):
    user_id: int
    movie_id: int
    reviews: str
    score: int

class ReviewResponseModel(ResponseModel):
    id: int
    user: UserResponseModel
    movie: MovieResponseModel
    reviews: str
    score: int
    
class ReviewRequestPutModel(BaseModel, ReviewValidator):
    reviews: str
    score: int
    


from fastapi import APIRouter, HTTPException
from project.database import User, Movie, UserReview
from project.schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel
from typing import List

router = APIRouter(prefix='/reviews')

@router.post("", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(404, "El usuario no existe")
    
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(404, "La pelicula no existe")
    
    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        reviews=user_review.reviews,
        score=user_review.score
    )
    
    return user_review

@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit)
    
    return [user_review for user_review in reviews]

@router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    review = UserReview.select().where(UserReview.id == review_id).first()
    
    if review is None:
        raise HTTPException(404, "La review no existe")
    
    return review

@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    review = UserReview.select().where(UserReview.id == review_id).first()
    
    if review is None:
        raise HTTPException(404, "La review no existe")
    
    review.reviews = review_request.reviews
    review.score = review_request.score
    
    review.save()
    
    return review

@router.delete('/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    review = UserReview.select().where(UserReview.id == review_id).first()
    
    if review is None:
        raise HTTPException(404, "La review no existe")
    
    review.delete_instance()
    
    return review
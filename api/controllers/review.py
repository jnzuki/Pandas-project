from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import review as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_review = model.Review(
        customer_id=request.customer_id,
        # dish_id=request.dish_id,
        menu_item_id=request.menu_item_id,

        rating=request.rating,
        # comment=request.comment,
        # created_at=request.created_at
        review_date=request.review_date,
        review_text=request.review_text
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


def read_all(db: Session):
    try:
        reviews = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews


def read_one(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review


def update(db: Session, review_id: int, request):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        update_data = request.dict(exclude_unset=True)
        review.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review.first()


def delete(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        review.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

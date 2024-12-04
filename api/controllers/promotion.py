from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import promotion as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_promotion = model.Promotion(
        code=request.code,
        discount_amount=request.discount_amount,
        expiration_date=request.expiration_date,
        is_active=request.is_active
    )

    try:
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_promotion


def read_all(db: Session):
    try:
        promotions = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotions


def read_one(db: Session, promotion_id: int):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion


def update(db: Session, promotion_id: int, request):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id)
        if not promotion.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion ID not found!")
        update_data = request.dict(exclude_unset=True)
        promotion.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion.first()


def delete(db: Session, promotion_id: int):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id)
        if not promotion.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion ID not found!")
        promotion.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

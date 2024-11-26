from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from models import ingredient as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_ingredient = model.Ingredient(
        name=request.name,
        quantity=request.quantity,
        unit=request.unit
    )

    try:
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_ingredient


def read_all(db: Session):
    try:
        ingredients = db.query(model.Ingredient).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredients


def read_one(db: Session, ingredient_id: int):
    try:
        ingredient = db.query(model.Ingredient).filter(model.Ingredient.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredient


def update(db: Session, ingredient_id: int, request):
    try:
        ingredient = db.query(model.Ingredient).filter(model.Ingredient.id == ingredient_id)
        if not ingredient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient ID not found!")
        update_data = request.dict(exclude_unset=True)
        ingredient.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return ingredient.first()


def delete(db: Session, ingredient_id: int):
    try:
        ingredient = db.query(model.Ingredient).filter(model.Ingredient.id == ingredient_id)
        if not ingredient.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient ID not found!")
        ingredient.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

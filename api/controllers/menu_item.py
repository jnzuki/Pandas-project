from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_item as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_menu_item = model.MenuItem(
        name=request.name,
        description=request.description,
        price=request.price,
        category=request.category,
        calories=request.calories,
        # is_spicy=request.is_spicy,
        # is_vegetarian=request.is_vegetarian,
        # is_kids_friendly=request.is_kids_friendly
        is_available=request.is_available
    )

    try:
        db.add(new_menu_item)
        db.commit()
        db.refresh(new_menu_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_menu_item


def read_all(db: Session):
    try:
        menu_items = db.query(model.MenuItem).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_items


def read_one(db: Session, menu_item_id: int):
    try:
        menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu Item ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item


def update(db: Session, menu_item_id: int, request):
    try:
        menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id)
        if not menu_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu Item ID not found!")
        update_data = request.dict(exclude_unset=True)
        menu_item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item.first()


def delete(db: Session, menu_item_id: int):
    try:
        menu_item = db.query(model.MenuItem).filter(model.MenuItem.id == menu_item_id)
        if not menu_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu Item ID not found!")
        menu_item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_detail as model
from ..models.ingredient import Ingredient
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    # Step 1: Create the OrderDetail object
    new_order_detail = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=request.quantity,
        subtotal=request.subtotal
    )

    # Step 2: Calculate ingredient requirements based on the menu item and quantity
    ingredient_requirements = new_order_detail.calculate_ingredients_needed(db)

    # Step 3: Check if there are enough ingredients in stock
    for ingredient_id, required_quantity in ingredient_requirements.items():
        ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ingredient with ID {ingredient_id} not found!"
            )
        if ingredient.quantity < required_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for ingredient '{ingredient.name}'. Required: {required_quantity}, Available: {ingredient.quantity}"
            )

    # Step 4: Deduct the required quantity of each ingredient from the stock
    for ingredient_id, required_quantity in ingredient_requirements.items():
        ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        ingredient.quantity -= required_quantity
        db.add(ingredient)

    # Step 5: Add the new order detail and commit the changes
    try:
        db.add(new_order_detail)
        db.commit()
        db.refresh(new_order_detail)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order_detail

def read_all(db: Session):
    try:
        order_details = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order_details


def read_one(db: Session, order_detail_id: int):
    try:
        order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id).first()
        if not order_detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Detail ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order_detail


def update(db: Session, order_detail_id: int, request):
    try:
        order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id)
        if not order_detail.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Detail ID not found!")
        update_data = request.dict(exclude_unset=True)
        order_detail.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order_detail.first()


def delete(db: Session, order_detail_id: int):
    try:
        order_detail = db.query(model.OrderDetail).filter(model.OrderDetail.id == order_detail_id)
        if not order_detail.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order Detail ID not found!")
        order_detail.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

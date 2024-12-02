from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_detail as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_order_detail = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=request.quantity,
        price=request.price
    )

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

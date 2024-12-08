from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order as model
from ..models.sales_report import SalesReport
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func



def create(db: Session, request):
    new_order = model.Order(
        customer_id=request.customer_id,
        order_date=request.order_date,
        # total_price=request.total_price,
        total_amount=request.total_amount,
        promotion_id=request.promotion_id,
        status=request.status,
        # delivery_address=request.delivery_address,
        delivery_type=request.delivery_type
        # is_takeout=request.is_takeout
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order


def read_all(db: Session):
    try:
        orders = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return orders


def read_one(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order

def read_by_date(db: Session, order_date: str):
    try:
        orders = db.query(model.Order).filter(
            func.date(model.Order.order_date) == order_date
        ).all()

        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found for this date!"
            )
    
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return orders

def read_by_date_range(db: Session, start_date: str, end_date: str):
    try:
        # Query orders within the date range (inclusive of both start and end dates)
        orders = db.query(model.Order).filter(
            func.date(model.Order.order_date) >= start_date,
            func.date(model.Order.order_date) <= end_date
        ).all()

        if not orders:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found for this date range!"
            )
    
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return orders

def update(db: Session, order_id: int, request):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
        update_data = request.dict(exclude_unset=True)
        order.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def get_total_revenue_by_date(db: Session, order_date: str):
    try:
        # sum of total_amount
        total_revenue = db.query(func.sum(model.Order.total_amount)).filter(
            func.date(model.Order.order_date) == order_date
        ).scalar()

        if total_revenue is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No revenue found for the specified date!"
            )

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return {"total_revenue": total_revenue}


def delete(db: Session, order_id: int):
    try:
        order = db.query(model.Order).filter(model.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order ID not found!")
        order.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

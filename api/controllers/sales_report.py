from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models.sales_report import SalesReport


from ..models import sales_report as model
from ..models import order as order_model

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func



def create(db: Session, request):
    new_report = model.SalesReport(
        date=request.date,
        # total_sales=request.total_sales,
        total_revenue=request.total_revenue,
        total_orders=request.total_orders
        # total_items_sold=request.total_items_sold
    )

    try:
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_report


def get_daily_revenue(db: Session, order_date: str):
    try:
        total_revenue = db.query(func.sum(order_model.Order.total_amount)).filter(
            func.date(order_model.Order.order_date) == order_date
        ).scalar()

        if total_revenue is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No revenue found for the specified date!"
            )

        sales_report = SalesReport(
            date=order_date,
            total_revenue=total_revenue
        )

        db.add(sales_report)
        db.commit()
        db.refresh(sales_report)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {"total_revenue": total_revenue}


def read_one(db: Session, report_id: int):
    try:
        report = db.query(model.SalesReport).filter(model.SalesReport.id == report_id).first()
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return report


def update(db: Session, report_id: int, request):
    try:
        report = db.query(model.SalesReport).filter(model.SalesReport.id == report_id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report ID not found!")
        update_data = request.dict(exclude_unset=True)
        report.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return report.first()


def delete(db: Session, report_id: int):
    try:
        report = db.query(model.SalesReport).filter(model.SalesReport.id == report_id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report ID not found!")
        report.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

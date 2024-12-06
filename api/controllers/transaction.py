from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import transaction as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_transaction = model.Transaction(
        # order_id=request.order_id,
        customer_id=request.customer_id,
        card_number=request.card_number,
        transaction_type=request.transaction_type,
        # payment_method=request.payment_method,
        amount=request.amount,
        transaction_date=request.transaction_date,
        balance_after_transaction=request.balance_after_transaction
    )

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_transaction


def read_all(db: Session):
    try:
        transactions = db.query(model.Transaction).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return transactions


def read_one(db: Session, transaction_id: int):
    try:
        transaction = db.query(model.Transaction).filter(model.Transaction.id == transaction_id).first()
        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return transaction


def update(db: Session, transaction_id: int, request):
    try:
        transaction = db.query(model.Transaction).filter(model.Transaction.id == transaction_id)
        if not transaction.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction ID not found!")
        update_data = request.dict(exclude_unset=True)
        transaction.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return transaction.first()


def delete(db: Session, transaction_id: int):
    try:
        transaction = db.query(model.Transaction).filter(model.Transaction.id == transaction_id)
        if not transaction.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction ID not found!")
        transaction.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

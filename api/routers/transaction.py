from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import transaction as controller
from ..schemas import transaction as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Transaction"],
    prefix="/transactions"
)


@router.post("/", response_model=schema.Transaction)
def create(request: schema.TransactionCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Transaction])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{transaction_id}", response_model=schema.Transaction)
def read_one(transaction_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, transaction_id=transaction_id)


@router.put("/{transaction_id}", response_model=schema.Transaction)
def update(transaction_id: int, request: schema.TransactionUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, transaction_id=transaction_id)


@router.delete("/{transaction_id}")
def delete(transaction_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, transaction_id=transaction_id)

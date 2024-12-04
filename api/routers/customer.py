from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import customer as controller
from ..schemas import customer as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Customer'],
    prefix="/customer"
)

# Create a new customer (Guest Orders)
@router.post("/", response_model=schema.Customer)
def create_customer(request: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

# Read all customers
@router.get("/", response_model=list[schema.Customer])
def read_all_customers(db: Session = Depends(get_db)):
    return controller.read_all(db)

# Read a single customer by ID
@router.get("/{customer_id}", response_model=schema.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, customer_id=customer_id)

# Update a customer's information
@router.put("/{customer_id}", response_model=schema.Customer)
def update_customer(customer_id: int, request: schema.CustomerUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, customer_id=customer_id, request=request)

# Delete a customer
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, customer_id=customer_id)

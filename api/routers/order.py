from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import order as controller
from ..schemas import order as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Order"],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{order_id}", response_model=schema.Order)
def read_one(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, order_id=order_id)

@router.get("/orders/date/{order_date}")
async def read_orders_by_date(order_date: str, db: Session = Depends(get_db)):
    return controller.read_by_date(db=db, order_date=order_date)

@router.get("/orders-by-date-range/{start_date}/{end_date}")
def read_orders_by_date_range(
    start_date: str, 
    end_date: str, 
    db: Session = Depends(get_db)
):
    return controller.read_by_date_range(db=db, start_date=start_date, end_date=end_date)

@router.get("/revenue/{order_date}", response_model=dict)
def get_revenue_by_date(order_date: str, db: Session = Depends(get_db)):
    return controller.get_total_revenue_by_date(db=db, order_date=order_date)

@router.put("/{order_id}", response_model=schema.Order)
def update(order_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)


@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, order_id=order_id)

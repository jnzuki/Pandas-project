from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import sales_report as controller
from ..schemas import sales_report as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Sales Report"],
    prefix="/sales-reports"
)


@router.post("/", response_model=schema.SalesReport)
def create(request: schema.SalesReportCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.SalesReport])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{report_id}", response_model=schema.SalesReport)
def read_one(report_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, report_id=report_id)


@router.put("/{report_id}", response_model=schema.SalesReport)
def update(report_id: int, request: schema.SalesReportUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, report_id=report_id)


@router.delete("/{report_id}")
def delete(report_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, report_id=report_id)

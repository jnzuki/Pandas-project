from pydantic import BaseModel
from datetime import date
from typing import Optional

class SalesReportBase(BaseModel):
    date: date
    total_revenue: float
    total_orders: int

class SalesReportCreate(SalesReportBase):
    pass

class SalesReportUpdate(BaseModel):
    total_revenue: Optional[float] = None
    total_orders: Optional[int] = None

class SalesReport(SalesReportBase):
    id: int

    class Config:
        orm_mode = True

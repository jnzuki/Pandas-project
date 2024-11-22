from sqlalchemy import Column, Integer, Date, DECIMAL
from ..dependencies.database import Base

class SalesReport(Base):
    __tablename__ = "sales_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    total_revenue = Column(DECIMAL(10, 2), nullable=False, default=0.0)
    total_orders = Column(Integer, nullable=False, default=0)


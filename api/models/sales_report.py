from sqlalchemy import Column, Integer, Date, DECIMAL
from ..dependencies.database import Base
from sqlalchemy.orm import declarative_base


class SalesReport(Base):
    __tablename__ = "sales_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, unique=True, index=True)
    total_revenue = Column(Integer)

    def __repr__(self):
        return f"<SalesReport(id={self.id}, date={self.date}, total_revenue={self.total_revenue})>"


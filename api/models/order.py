from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)  # Links to Customer
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(50), nullable=False, default="pending")
    total_amount = Column(DECIMAL(10, 2), nullable=False, default=0.0)
    delivery_type = Column(String(50), nullable=False)  # e.x takeout or delivery

    customer = relationship("Customer", back_populates="orders")  # Links back to Customer
    order_details = relationship("OrderDetail", back_populates="order")  # One-to-Many with OrderDetail
    promotions = relationship("Promotion", secondary="order_promotions", back_populates="orders")  # Many-to-Many with Promotion

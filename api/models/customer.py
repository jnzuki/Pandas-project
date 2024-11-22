from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    card_number = Column(String(16), unique=True, nullable=False)  # Fake debit card number
    balance = Column(DECIMAL(10, 2), nullable=False, server_default="0.00")

    orders = relationship("Order", back_populates="customer")  # One-to-Many relationship with orders
    reviews = relationship("Review", back_populates="customer")  # One-to-Many relationship with reviews
    transactions = relationship("Transaction", back_populates="customer")  # One-to-Many with transactions

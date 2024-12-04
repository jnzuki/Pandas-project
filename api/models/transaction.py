from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from datetime import datetime
from ..dependencies.database import Base
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    card_number = Column(String(20), unique=True, nullable=False)
    transaction_type = Column(String(10), nullable=False)  # debit /  credit
    transaction_date = Column(DateTime, default=datetime.now())
    amount = Column(DECIMAL(10, 2), nullable=False)
    balance_after_transaction = Column(DECIMAL(10, 2), nullable=False)

    customer = relationship("Customer", foreign_keys=[customer_id])  # Links back to Customer

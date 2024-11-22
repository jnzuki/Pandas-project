from sqlalchemy import Column, Integer, String, DECIMAL, Date, Boolean
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_amount = Column(DECIMAL(10, 2), nullable=False)
    expiration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", secondary="order_promotions", back_populates="promotions")

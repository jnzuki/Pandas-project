from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)
    review_date = Column(DateTime, default=datetime.now())

    customer = relationship("Customer", back_populates="reviews")
    menu_item = relationship("MenuItem", back_populates="reviews")

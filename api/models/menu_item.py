from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Text
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True)  # e.x, spicy, vegetarian, kids,
    is_available = Column(Boolean, default=True)

    order_details = relationship("OrderDetail", back_populates="menu_item")  # Linked to OrderDetail
    reviews = relationship("Review", back_populates="menu_item")  # One-to-Many with reviews
    recipes = relationship("Recipe", back_populates="menu_item")  # Many-to-Many via Recipe

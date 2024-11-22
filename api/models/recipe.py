from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)  # Links to Menuitem
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)  # Links to Ingredient
    quantity = Column(DECIMAL(10, 2), nullable=False)

    menu_item = relationship("MenuItem", back_populates="recipes")  # Links back to MenuItem
    ingredient = relationship("Ingredient", back_populates="recipes")  # Links back to Ingredient

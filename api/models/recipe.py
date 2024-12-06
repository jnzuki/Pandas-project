from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)  # Links to Menuitem
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)  # Links to Ingredient
    quantity = Column(DECIMAL(10, 2), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)  # Links to Resource

    resource = relationship("Resource", back_populates="recipes") 

    menu_item = relationship("MenuItem", foreign_keys=[menu_item_id])  # Links back to MenuItem
    ingredient = relationship("Ingredient", foreign_keys=[ingredient_id])  # Links back to Ingredient
    resources = relationship("Resource", foreign_keys=[resource_id])  # One-to-Many with Resource
    
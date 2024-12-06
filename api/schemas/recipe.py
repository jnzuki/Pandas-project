from pydantic import BaseModel
from typing import Optional

class RecipeBase(BaseModel):
    menu_item_id: int
    ingredient_id: int
    quantity: float
    resource_id: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    ingredient_id: Optional[int] = None
    quantity: Optional[float] = None

class Recipe(RecipeBase):
    id: int

    class Config:
        orm_mode = True

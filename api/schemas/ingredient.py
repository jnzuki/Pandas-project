from typing import Optional, List
from pydantic import BaseModel
# from recipe import Recipe

class IngredientBase(BaseModel):
    name: str
    stock_level: int
    unit: Optional[str] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    stock_level: Optional[int] = None
    unit: Optional[str] = None

class Ingredient(IngredientBase):
    id: int
    # recipes: Optional[List[Recipe]] = None

    class Config:
        orm_mode = True

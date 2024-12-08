from typing import Optional, List
from pydantic import BaseModel
# from recipe import Recipe

class IngredientBase(BaseModel):
    name: str
    quantity: int
    unit: Optional[str] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None

class Ingredient(IngredientBase):
    id: int

    class Config:
        orm_mode = True

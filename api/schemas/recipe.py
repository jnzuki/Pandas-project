from pydantic import BaseModel
from typing import Optional, List

class RecipeBase(BaseModel):
    menu_item_id: int
    ingredient_id: List[int] 
    quantity: List[int]  

class RecipeCreate(BaseModel):
    menu_item_id: int
    ingredient_id: List[int]
    quantity: List[int]
    
class RecipeUpdate(BaseModel):
    menu_item_id: Optional[int] = None
    ingredient_id: Optional[dict] = None
    quantity: Optional[int] = None

class RecipeResponse(BaseModel):
    id: int
    menu_item_id: int
    ingredient_id: int
    quantity: int
    class Config:
        orm_mode = True
        from_attributes = True


class Recipe(RecipeBase):
    id: int



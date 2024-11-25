from typing import Optional, List
from pydantic import BaseModel
from review import Review
from recipe import Recipe

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: Optional[int] = None
    category: Optional[str] = None
    is_available: Optional[bool] = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None

class MenuItem(MenuItemBase):
    id: int
    reviews: Optional[List[Review]] = None
    recipes: Optional[List[Recipe]] = None

    class Config:
        orm_mode = True

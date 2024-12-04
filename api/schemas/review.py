from pydantic import BaseModel
from datetime import datetime
from typing import Optional
# from .menu_item import MenuItem
# from customer import Customer

class ReviewBase(BaseModel):
    rating: int
    review_text: Optional[str] = None
    review_date: Optional[datetime] = None
    customer_id: int
    menu_item_id: int


class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    review_text: Optional[str] = None
    review_date: Optional[datetime] = None
    # customer_id: Optional[int] = None
    menu_item_id: Optional[int] = None


class Review(ReviewBase):
    id: int
    # customer: Customer
    # menu_item: MenuItem

    class Config:
        orm_mode = True

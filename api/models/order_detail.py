from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)  # Links to Order
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)  # Links to MenuItem
    quantity = Column(Integer, nullable=False, default=1)
    subtotal = Column(DECIMAL(10, 2), nullable=False)  # (price × quantity)

    order = relationship("Order", foreign_key=[order_id])  # Links back to Order
    menu_item = relationship("MenuItem", foreign_key=[menu_item_id])  # Links back to MenuItem

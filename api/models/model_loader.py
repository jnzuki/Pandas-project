from . import customers, menu_items, ingredients, recipes, orders, order_details, promotions, reviews, sales_reports, transactions

from ..dependencies.database import engine


def index():
    customers.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    ingredients.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    sales_reports.Base.metadata.create_all(engine)
    transactions.Base.metadata.create_all(engine)

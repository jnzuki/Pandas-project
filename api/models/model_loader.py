# from . import customer, menu_item, ingredient, recipe, order, order_detail, promotion, review, sales_report, transaction

# from ..dependencies.database import engine
from . import customer, menu_item, ingredient, recipe, order, order_detail, promotion, review, sales_report, transaction

from ..dependencies.database import engine



# def index():
#     customer.Base.metadata.create_all(engine)
#     menu_item.Base.metadata.create_all(engine)
#     ingredient.Base.metadata.create_all(engine)
#     recipe.Base.metadata.create_all(engine)
#     order.Base.metadata.create_all(engine)
#     order_detail.Base.metadata.create_all(engine)
#     promotion.Base.metadata.create_all(engine)
#     review.Base.metadata.create_all(engine)
#     sales_report.Base.metadata.create_all(engine)
#     transaction.Base.metadata.create_all(engine)
def index():
    customer.Base.metadata.create_all(engine)
    menu_item.Base.metadata.create_all(engine)
    ingredient.Base.metadata.create_all(engine)
    recipe.Base.metadata.create_all(engine)
    order.Base.metadata.create_all(engine)
    order_detail.Base.metadata.create_all(engine)
    promotion.Base.metadata.create_all(engine)
    review.Base.metadata.create_all(engine)
    sales_report.Base.metadata.create_all(engine)
    transaction.Base.metadata.create_all(engine)

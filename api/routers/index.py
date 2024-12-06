from . import order, order_detail, menu_item, customer, promotion, review, recipe, ingredient, sales_report, transaction

def load_routes(app):
    app.include_router(order.router)
    app.include_router(order_detail.router)
    app.include_router(menu_item.router)
    app.include_router(customer.router)
    app.include_router(promotion.router)
    app.include_router(review.router)
    app.include_router(recipe.router)
    app.include_router(ingredient.router)
    app.include_router(sales_report.router)
    app.include_router(transaction.router)

    




#  menu_item, customer, review, recipe, ingredient, sales_report



# from . import order, order_detail, promotion, menu_item, customer, review, recipe, ingredient, sales_report


# def load_routes(app):
#     app.include_router(recipe.router)
#     app.include_router(ingredient.router)

from . import order, order_detail


def load_routes(app):
    app.include_router(order.router)
    app.include_router(order_detail.router)

from . import models
from . import wizard


def post_init_hook(env):
    """Generate missing stock.lot.rental entries for existing records."""
    lots = env["stock.lot"].search([("product_id.rent_ok", "=", True)])
    lots._create_stock_rental_lot()
    lines = env["sale.order.line"].search([("is_rental", "=", True)])
    lines._create_stock_rental_lot()

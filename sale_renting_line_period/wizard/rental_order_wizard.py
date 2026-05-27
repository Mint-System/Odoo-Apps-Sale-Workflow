# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class RentalOrderWizard(models.TransientModel):
    _inherit = "rental.order.wizard"

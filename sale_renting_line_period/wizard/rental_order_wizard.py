# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class RentalOrderWizard(models.TransientModel):
    _inherit = "rental.order.wizard"

    def apply(self):
        """
        Upate line return date and split order lines if partial qty is returned.
        """
        res = super().apply()
        for wizard in self:
            _logger.warning(wizard.rental_wizard_line_ids)
        return

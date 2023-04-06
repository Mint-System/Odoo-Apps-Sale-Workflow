from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    def action_view_so(self):
        self.ensure_one()
        action = self.env.ref('sale.action_orders')
        result = action.read()[0]
        result['context'] = {}
        result['domain'] = [('project_id', '=', self.id)]
        return result

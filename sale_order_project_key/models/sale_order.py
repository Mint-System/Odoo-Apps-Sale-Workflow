from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        """Propagate saleder order data to linked project."""
        res = super()._action_confirm()
        # Write partner to project
        if self.project_id and not self.project_id.partner_id:
            self.project_id.write({
                'partner_id': self.partner_id.id,
            })
        # Write partner to projec tasks
        for task in self.project_id.task_ids.filtered(lambda t: not t.partner_id):
            task.write({
                'partner_id': self.partner_id.id,
            })
        return res 

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.project_id.code != '/':
            self.name = self.project_id.code
        else:
            self.name = _('New')

        
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    project_id = fields.Many2one(compute='_compute_project_id', store=True)

    @api.depends('order_id.project_id')
    def _compute_project_id(self):
        self.project_id =  self.order_id.project_id

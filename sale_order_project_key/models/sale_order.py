from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def create(self, vals):
    #     """Use project key as name for sale order."""
        
    #     if vals.get('project_id'):
    #         project = self.env['project.project'].browse(vals.get('project_id'))
    #         if project.code:
    #             vals['name'] = project.code
    #     res = super(SaleOrder, self).create(vals)

    #     # Update sale order link on project      
    #     if res.project_id:
    #         res.project_id.write({
    #             'partner_id': res.partner_id.id,
    #         })
        
    #     return res

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id and self.project_id.code != '/':
            self.name = self.project_id.code
        else:
            self.name = _('New')
        
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        """Propagate sale order data to linked project."""
        res = super()._action_confirm()
        # Write partner to project
        if self.project_id and not self.project_id.partner_id:
            self.project_id.write({
                'partner_id': self.partner_id.id,
            })
        # Write partner to project tasks
        for task in self.project_id.task_ids.filtered(lambda t: not t.partner_id):
            task.write({
                'partner_id': self.partner_id.id,
            })
        # Write analytic account to linked projects
        if self.project_ids:
            self.project_ids.write({
                'analytic_account_id': self.analytic_account_id.id,
            })
        return res 

    def name_get(self):
        res = super(SaleOrder, self).name_get()
        for rec in self.filtered(lambda r: r.project_id and r.partner_id):
            # Remove existing entry
            res = list(filter(lambda t: t[0] != rec.id, res))
            res.append((rec.id, '[%s] %s - %s' % (rec.project_id.code, rec.name, rec.partner_id.name)))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        # Search in project code and partner name
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        elif operator in ('ilike', 'like', '=', '=like', '=ilike'):
            domain = expression.AND([
                args or [],
                ['|', ('name', operator, name),'|', ('project_id.code', operator, name), ('partner_id.name', operator, name)]
            ])
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    def action_view_task(self):
        """Remove sale order default search from context."""
        res = super().action_view_task()
        if res.get('context'):
            res['context'].pop('search_default_sale_order_id', False)
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    project_id = fields.Many2one(compute='_compute_project_id', store=True)

    @api.depends('order_id.project_id')
    def _compute_project_id(self):
        for rec in self:
            rec.project_id = rec.order_id.project_id

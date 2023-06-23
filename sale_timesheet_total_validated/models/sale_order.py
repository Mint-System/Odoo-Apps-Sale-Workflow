from odoo import _, api, fields, models
from collections import defaultdict
import logging
_logger = logging.getLogger(__name__)
from odoo.addons.sale_timesheet_enterprise.models.sale import DEFAULT_INVOICED_TIMESHEET


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('company_id.project_time_mode_id', 'timesheet_ids', 'company_id.timesheet_encode_uom_id')
    def _compute_timesheet_total_duration(self):
        """Filter validated analytic lines"""
        super()._compute_timesheet_total_duration()
        param_invoiced_timesheet = self.env['ir.config_parameter'].sudo().get_param('sale.invoiced_timesheet', DEFAULT_INVOICED_TIMESHEET)
        if param_invoiced_timesheet == 'approved':
            group_data = self.env['account.analytic.line'].sudo().read_group([
                ('order_id', 'in', self.ids),
                ('validated', '=', True),
            ], ['order_id', 'unit_amount'], ['order_id'])
            timesheet_unit_amount_dict = defaultdict(float)
            timesheet_unit_amount_dict.update({data['order_id'][0]: data['unit_amount'] for data in group_data})
            for sale_order in self:
                total_time = sale_order.company_id.project_time_mode_id._compute_quantity(timesheet_unit_amount_dict[sale_order.id], sale_order.timesheet_encode_uom_id)
                sale_order.timesheet_total_duration = round(total_time)

    def action_view_timesheet(self):
        action = super().action_view_timesheet()
        param_invoiced_timesheet = self.env['ir.config_parameter'].sudo().get_param('sale.invoiced_timesheet', DEFAULT_INVOICED_TIMESHEET)
        if param_invoiced_timesheet == 'approved':
            action['context']['search_default_validated'] = True
        return action
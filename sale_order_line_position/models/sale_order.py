import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class Document(models.Model):
    _name = 'sale_order_line_position.document'
    _description = 'Sale order line position Document'

    # fields
    name = fields.Char()
    value = fields.Integer()
from odoo import api, models, fields

class Customer(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(string="Customer Code")




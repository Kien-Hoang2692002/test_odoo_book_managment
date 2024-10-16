from odoo import api, models, fields

class Publisher(models.Model):
    _name = 'publisher'
    _description = 'Publisher Model'

    name = fields.Char(string="Publisher Name", required=True)
    book_ids = fields.One2many('book', 'publisher_id', string="Published Books")
    
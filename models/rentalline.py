from odoo import api, models, fields
from odoo.exceptions import ValidationError

class RentalLine(models.Model):
    _name = 'book.rental.line'
    _description = 'Book Rental Line'

    rental_id = fields.Many2one('book.rental', string='Rental')
    book_id = fields.Many2one('book', string='Book', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Float(string='Price per Unit')

    @api.onchange('book_id')
    def _onchange_book_id(self):
        if self.book_id:
            self.price_unit = self.book_id.rental_price
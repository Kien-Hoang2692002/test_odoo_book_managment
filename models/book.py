from odoo import api, models, fields
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = 'book'
    _description = 'Book Model'

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Image", attachment=True)
    author_id = fields.Many2one('author', string="Author", required=True)
    category_ids = fields.Many2many('book.category', string="Categories")
    publisher_id = fields.Many2one('publisher', string="Publisher")
    published_date = fields.Date(string="Published Date")
    page_count = fields.Integer(string="Page Count")
    rental_price = fields.Float(string="Rental Price")
    state = fields.Selection([('draft', 'Draft'), ('published', 'Published')], default='draft')
    quantity_base = fields.Integer(string='Quantity Base', default=1)
    quantity_rental = fields.Integer(string='Quantity Rental', default=0)
    available = fields.Boolean('Available', compute='_compute_availability', store=True)

    def action_confirm(self):
        self.state = 'published'

    @api.depends('quantity_base', 'quantity_rental')
    def _compute_availability(self):
        for record in self:
            record.available = record.quantity_base > record.quantity_rental

    @api.constrains('quantity_base', 'quantity_rental')
    def _check_quantity(self):
        for record in self:
            if record.quantity_base <= 0:
                raise ValidationError("Quantity must be greater than zero.")
            if record.quantity_base < record.quantity_rental:
                raise ValidationError("Quantity Base must be greater than or equal to Quantity Rental.")

    @api.constrains('rental_price')
    def _check_rental_price(self):
        for record in self:
            if record.rental_price <= 0:
                raise ValidationError("Rental price must be greater than zero.")

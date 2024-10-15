from odoo import api, models, fields

class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'Book Category Model'

    name = fields.Char(string="Category Name", required=True)
    book_ids = fields.Many2many('book', string="Books")

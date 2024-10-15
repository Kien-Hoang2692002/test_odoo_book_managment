from odoo import api, models, fields
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
import re

class Author(models.Model):
    _name = 'author'
    _description = 'Author Model'

    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string='Phone Number', size=10)
    nationality = fields.Char(string="Nationality")
    book_ids = fields.One2many('book', 'author_id', string="Books")
    book_count = fields.Integer(string='Book Count', compute='_compute_book_count', store=True)

    @api.constrains('phone')
    def _check_phone_number(self):
        # Vietnamese phone number regex pattern
        vietnam_phone_pattern = re.compile(r'^(09|03|07|08|05)\d{8}$')
        for record in self:
            if record.phone and not vietnam_phone_pattern.match(record.phone):
                raise ValidationError(
                    "Phone number must be a valid Vietnamese number (10 digits, starting with 09, 03, 07, 08, or 05).")
                # raise Warning("Please enter a phone")

    @api.depends('book_ids')
    def _compute_book_count(self):
        for record in self:
            record.book_count = len(record.book_ids)
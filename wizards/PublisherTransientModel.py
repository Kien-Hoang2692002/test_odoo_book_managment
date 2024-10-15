from odoo import api, models, fields
from odoo.exceptions import ValidationError

class PublisherTransient(models.TransientModel):
    _name = 'publishertransient'
    _description = 'Publisher Transient Model'

    name = fields.Char(string="Publisher Name")

    def create_publisher(self):
        if not self.name:
            raise ValidationError("Publisher Name is required")
        self.env['publisher'].create({'name': self.name})





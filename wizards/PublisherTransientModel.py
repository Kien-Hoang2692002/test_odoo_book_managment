from odoo import api, models, fields

class PublisherTransient(models.TransientModel):
    _name = 'publishertransient'
    _description = 'Publisher Transient Model'

    name = fields.Char(string="Publisher Name")


    def edit_publisher(self):
        active_id = self.env.context.get('active_id')
        publisher = self.env['publisher'].browse(active_id)
        if not publisher.exists():
            raise ValueError(f"Publisher record with ID {active_id} does not exist.")
        if not self.name:
            raise ValueError("The field 'name' is empty.")
        print(publisher)
        publisher.write({'name': self.name})





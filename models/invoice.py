from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BookRentalInvoice(models.Model):
    _name = 'book.rental.invoice'
    _description = 'Book Rental Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    rental_id = fields.Many2one('book.rental', string='Rental', required=True)
    total_rental_price = fields.Float(string='Total Rental Price', related='rental_id.total_rental_price')
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ], default='pending')

    def action_pay_invoice(self):
        for record in self:
            # Kiểm tra xem hóa đơn có đang ở trạng thái 'pending' không
            if record.payment_status == 'pending':
                # Cập nhật trạng thái thanh toán
                record.payment_status = 'paid'

                # Kiểm tra xem có liên kết đến rental_id không
                if record.rental_id:
                    # Cập nhật trạng thái của rental_id
                    if record.rental_id.state_rental != 'paid':
                        record.rental_id.state_rental = 'paid'
                    else:
                        raise ValidationError(("This rental is already marked as paid."))

                # Thêm thông báo cho người dùng khi thanh toán thành công
                record.message_post(body=("Invoice has been paid."))
            else:
                raise ValidationError(("This invoice has already been paid."))

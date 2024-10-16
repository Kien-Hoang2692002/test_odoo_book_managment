from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Rental(models.Model):
    _name = 'book.rental'
    _description = 'Book Rental Model'

    book_id = fields.Many2one('book', string="Book", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer Rental", required=True)
    rental_date = fields.Date(string="Rental Date", default=fields.Date.context_today, required=True)
    return_date = fields.Date(string="Return Date")
    rental_price = fields.Float(string="Rental Price", related='book_id.rental_price')
    total_rental_price = fields.Float(string="Total Rental Price", compute='_compute_total_rental_price', store=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('waiting', 'Waiting for Approval'),
                              ('ongoing', 'Ongoing'),
                              ('returned', 'Returned'),
                              ('overdue', 'Overdue'),
                              ('rejected', 'Rejected')],
                             default='draft')
    state_rental = fields.Selection([('draft', 'Draft'),
                                    ('confirmed', 'Confirmed'),
                                    ('paid', 'Paid'),
                                    ('cancelled', 'Cancelled'),
                                    ], default='draft')

    @api.constrains('rental_date', 'return_date')
    def _check_dates(self):
        for record in self:
            if record.return_date < record.rental_date:
                raise ValidationError("Return date cannot be earlier than rental date.")

    @api.depends('rental_date', 'return_date', 'rental_price')
    def _compute_total_rental_price(self):
        for record in self:
            if record.rental_date and record.return_date:
                # Tính số ngày thuê
                rental_days = (record.return_date - record.rental_date).days + 1
                if rental_days < 0:
                    rental_days = 0
                # Tính tổng giá thuê
                record.total_rental_price = rental_days * record.rental_price
            else:
                record.total_rental_price = 0

    @api.depends('state')
    def _compute_css_class(self):
        for record in self:
            record.css_class = 'oe_rental_' + record.state

    css_class = fields.Char(compute='_compute_css_class', store=False)

    def action_send_for_approval(self):
        self.state = 'waiting'

    def action_approve(self):
        if self.book_id.quantity_base <= self.book_id.quantity_rental:
            raise ValidationError("Not enough books available for rental.")
        self.book_id.quantity_rental += 1
        self.book_id.sudo().write({'quantity_rental': self.book_id.quantity_rental})

        self.state = 'ongoing'
        if self.book_id.quantity_base <= self.book_id.quantity_rental:
            self.book_id.available = False
         # Gửi email thông báo cho khách hàng
        print('Sending email...')
        template = self.env.ref('book_managment.email_template_rental_approved')
        
        # Kiểm tra template có tồn tại không
        if not template:
            raise ValidationError("Email template not found.")
        # In ra email của người nhận để kiểm tra
        print(f"Recipient email: {self.customer_id.email}")
        # Gửi email
        template.send_mail(self.id, force_send=True)
        print('Email sent successfully')

    def action_reject(self):
        self.state = 'rejected'

    def action_return(self):
        if self.book_id.quantity_rental > 0:
            self.book_id.quantity_rental -= 1
        self.book_id.sudo().write({'quantity_rental': self.book_id.quantity_rental})
        self.book_id.available = True
        self.state = 'returned'

    @api.model
    def create(self, vals):
        book = self.env['book'].browse(vals['book_id'])

        if book.quantity_base <= book.quantity_rental:
            raise ValidationError("Not enough books available for rental.")

        return super(Rental, self).create(vals)
    
    @api.model
    def auto_update_rental_status(self):
        today = fields.Date.today()
        overdue_rentals = self.search([('return_date', '<=', today), ('state', '=', 'ongoing')])

        for rental in overdue_rentals:
            rental.write({'state': 'overdue'})

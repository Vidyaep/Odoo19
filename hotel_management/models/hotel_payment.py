from odoo import fields, models, api
class HotelPayment(models.Model):
    _name = 'hotel.payment'
    _description = 'Hotel Payment'

    accommodation_id = fields.Many2one('hotel.accommodation',string="Accommodation",ondelete='cascade')
    name = fields.Char(string='Name')
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
    payment_line_ids = fields.One2many('hotel.payment.line', 'payment_id', string="Payment Lines")
    total_amount = fields.Float(string="Total", compute="_compute_total")

    @api.depends('payment_line_ids.price')
    def _compute_total(self):
        """Function to calculate total amount"""
        for record in self:
            record.total_amount = sum(record.payment_line_ids.mapped('price'))


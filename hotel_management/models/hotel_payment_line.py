from odoo import fields, models
class HotelPaymentLine(models.Model):
    _name = 'hotel.payment.line'
    _description = 'Hotel Payment Line'

    payment_id = fields.Many2one('hotel.payment', string="Payment Reference")
    accommodation_id = fields.Many2one('hotel.accommodation', string="Accommodation",ondelete='cascade')
    name = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity", default=1)
    price = fields.Float(string="Price")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
from odoo import fields, models
class HotelGuest(models.Model):
    _name = 'hotel.guest'

    guest_id = fields.Many2one('hotel.accommodation',string='Guest')
    name = fields.Many2one('res.partner',string="Name")
    gender = fields.Selection([('male','male'),('female','female'),('other','Other')],string='Gender')
    age = fields.Integer('Age')
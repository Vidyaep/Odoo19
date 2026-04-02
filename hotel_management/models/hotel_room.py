from email.policy import default

from odoo import fields, models

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _rec_name = 'room_no'
    room_no = fields.Char(string="Room Number")
    bed=fields.Selection(string="Beds", selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])
    available_beds = fields.Integer(string="Available Beds")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)
    rent=fields.Monetary(string="Rent",currency_field="currency_id")
    facility=fields.Many2many('hotel.facility',string="Facility")
    state = fields.Selection(string="State",readonly=True,default='available',tracking=True,required=True,selection=[('available', 'Available'), ('not_available', 'Not Available')])



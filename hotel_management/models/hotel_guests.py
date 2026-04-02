from odoo import api, fields, models
class HotelGuests(models.Model):
    _inherit = 'res.partner'

    hotel_guest = fields.Boolean(string="Is Hotel Guest",readonly=True,compute='compute_is_guest')
    accommodation_id = fields.Many2one('hotel.accommodation',string="Accommodation")

    @api.depends('accommodation_id.guests')
    def compute_is_guest(self):
        for record in self:
            partner = self.env['hotel.accommodation'].search([('guests', '=', record.id),('status','=','check-in')])
            if partner:
                record.hotel_guest = True
            else:
                record.hotel_guest = False
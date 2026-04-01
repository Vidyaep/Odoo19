from email.policy import default
from typing import Sequence

from odoo import api, fields, models
from odoo.orm.types import ValuesType


class HotelGuests(models.Model):
    _inherit = 'res.partner'

    hotel_guest = fields.Boolean(string="Is Hotel Guest",readonly=True,compute='compute_is_guest')
    accommodation_id = fields.Many2one('hotel.accommodation',string="Accommodation")

    # def default_get(self, fields_list):
    #     defaults = super().default_get(fields_list)
    #     if self.env.context.get('hotel_guest'):
    #         defaults['hotel_guest'] = True
    #     return defaults

    @api.depends('accommodation_id.guests')
    def compute_is_guest(self):
        for record in self:
            partner = self.env['hotel.accommodation'].search([('guests', '=', record.id),('status','=','check-in')])
            if partner:
                record.hotel_guest = True
            else:
                record.hotel_guest = False
from odoo import fields, models

class HotelFacility(models.Model):
    _name = 'hotel.facility'
    name = fields.Char(string="Facility Name")

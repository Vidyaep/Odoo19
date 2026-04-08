from odoo import fields, models

class HotelFacility(models.Model):
    _name = 'hotel.facility'
    name = fields.Char(string="Facility Name")
    company_id = fields.Many2one('res.company', string="Company",  default=lambda self: self.env.company)

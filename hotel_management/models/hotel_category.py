from odoo import fields, models

class HotelCategory(models.Model):
    _name = 'hotel.category'
    name = fields.Char(string="Category Name")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
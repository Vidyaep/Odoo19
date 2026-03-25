from odoo import fields, models

class HotelCategory(models.Model):
    _name = 'hotel.category'
    name = fields.Char(string="Category Name")
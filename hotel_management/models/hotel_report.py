from odoo import api, fields, models
class HotelReport(models.TransientModel):
    _name = 'hotel.report'
    date_from = fields.Datetime(required=True,string='Date from')
    date_to = fields.Datetime(required=True,string='Date to')
    guest_name = fields.Many2one('res.partner',string='Guest Name')

    def generate(self):
        for record in self:
            if record.guest_name and record.date_from and record.date_to:


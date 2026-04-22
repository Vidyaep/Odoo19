from odoo import api, fields, models
from odoo.exceptions import UserError


class HotelReport(models.TransientModel):
    _name = 'hotel.report'
    date_from = fields.Date(required=True,string='Date from')
    date_to = fields.Date(required=True,string='Date to')
    guest_name = fields.Many2one('res.partner',string='Guest Name')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)

    def generate(self):
        # print(self.read()[0])
        query = """select a.sequence,a.guests,r.name,a.check_in,a.check_out,a.status from hotel_accommodation as a left join res_partner as r on a.guests=r.id where a.guests = %s"""
        self.env.cr.execute(query,self.guest_name.id,)
        results = self.env.cr.dictfetchall()
        print(results)
        if results:
           return self.env.ref('hotel_management.action_hotel_management_report').report_action(results)
        else:
            raise UserError("No result found")


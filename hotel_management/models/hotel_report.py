from time import strptime

from odoo import api, fields, models
from odoo.addons.test_convert.tests.test_env import data
from odoo.exceptions import UserError


class HotelReport(models.TransientModel):
    _name = 'hotel.report'
    _description = 'Hotel Report Model'
    date_from = fields.Date(required=True,string='Date from')
    date_to = fields.Date(required=True,string='Date to')
    guest_name = fields.Many2one('res.partner',string='Guest Name')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.company)

    def generate(self):
        # print(self.read()[0])
        query = """select a.sequence,r.name,a.check_in,a.check_out,a.status from hotel_accommodation as a left join res_partner as r on a.guests=r.id where a.active=True"""
        if self.guest_name:
            query += """ and a.guests = %s""" %(self.guest_name.id)
            # self.env.cr.execute(query, (self.guest_name.id,))
        # date_from = str(self.date_from)
        # date_checkin = strptime(date_from, '%Y-%m-%d')
        if self.date_from:
            query += """ and a.check_in >= '%s' and a.check_out < '%s'""" %(self.date_from, self.date_to)
        #     # self.env.cr.execute(query,(self.date_from,))
        # date_to = str(self.date_to)
        # date_checkout = strptime(date_to, '%Y-%m-%d')
        # if self.date_to:
        #     query += """ and a.check_out >= '%s'""" %(self.date_to)
        #     # self.env.cr.execute(query,(self.date_to,))
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()
        print(results)
        return results

    def cancel(self):
        self.clear()
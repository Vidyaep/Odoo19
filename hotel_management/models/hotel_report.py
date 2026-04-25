from time import strptime
import json
from odoo import api, fields, models
from odoo.tools import json_default
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
        query = """select a.sequence,r.name,a.check_in,a.check_out,a.status from hotel_accommodation as a left join res_partner as r on a.guests=r.id"""
        if self.guest_name:
            query += """ where a.guests = %s""" %(self.guest_name.id)
        if self.date_from and self.date_to:
            query += """ and a.check_in >= '%s' and a.check_in <= '%s'""" %(self.date_from, self.date_to)
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()
        print(results)
        return results

    def generate_xlsx(self):
        query = """select a.sequence,r.name,a.check_in,a.check_out,a.status from hotel_accommodation as a left join res_partner as r on a.guests=r.id"""
        if self.guest_name:
            query += """ where a.guests = %s""" %(self.guest_name.id)
        if self.date_from and self.date_to:
            query += """ and a.check_in >= '%s' and a.check_in <= '%s'""" %(self.date_from, self.date_to)
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()
        data = {
            'results':results,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'hotel.report',
                     'options': json.dumps(data,default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Hotel Management Report',
                     },
            'report_type': 'xlsx',
        }
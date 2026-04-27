import io
import json
import xlsxwriter
from odoo import api, fields, models
from odoo.tools import json_default


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
        print(data)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'hotel.report',
                     'options': json.dumps(data,default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Hotel Management Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', 'align': 'center'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('A2:J3', 'HOTEL MANAGEMENT REPORT', head)
        sheet.merge_range('A4:B4', 'SL NO', cell_format)
        sheet.merge_range('C4:D4', 'GUEST', cell_format)
        sheet.merge_range('E4:F4', 'CHECK IN', cell_format)
        sheet.merge_range('G4:H4', 'CHECK OUT', cell_format)
        sheet.merge_range('I4:J4', 'STATUS', cell_format)
        for i, result in enumerate(data['results'],start=5):
            sheet.merge_range(f'A{i}:B{i}', result, txt)
        print("1")
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
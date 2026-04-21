from odoo import api, fields, models
class HotelReport(models.TransientModel):
    _name = 'hotel.report'
    date_from = fields.Date(required=True,string='Date from')
    date_to = fields.Date(required=True,string='Date to')
    guest_name = fields.Many2one('res.partner',string='Guest Name')

    def generate(self):
        print(self.read()[0])
        query = """select sequence,guests,check_in,check_out,status from hotel_accommodation where check_in >= '%s' and check_out <= '%s' and guests = '%s'""" % (self.date_from, self.date_to, self.guest_name.id)
        self.env.cr.execute(query)
        report = self.env.cr.fetchall()
        print(report)
        data = {
            'report': report,
            'form' : self.read()[0]
        }
        return self.env.ref('hotel_management.action_hotel_management_report').report_action(self,data=data)


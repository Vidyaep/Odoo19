from odoo import fields, models
class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'

    loan_id = fields.Many2one('employee.loan',string='Loan')
    date = fields.Datetime(string='Date')
    amount=fields.Float(string='Amount')
    paid =fields.Boolean(string='Paid')
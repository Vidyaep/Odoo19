from odoo import fields, models
class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    name = fields.Char('reference',required=True)
    employee_id = fields.Many2one('hr.employee',string='Employee')
    loan_amount = fields.Float(string='Loan Amount')
    installment_count=fields.Integer(string='Installment Count')
    start_date=fields.Datetime(string='Start Date')
    state = fields.Selection(selection_add=[('draft','Draft'),('approved','Approved'),('ongoing','Ongoing'),('paid','Paid')],string='State',default='draft')
    loan_line_ids=fields.One2many('employee.loan.line','employee_id',string='Loan Lines')

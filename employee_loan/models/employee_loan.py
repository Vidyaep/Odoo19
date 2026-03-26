from odoo import fields, models, api

class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan Model'
    name = fields.Char('reference',required=True,copy=False,tracking=True,default='New')
    employee_id = fields.Many2one('hr.employee',string='Employee')
    loan_amount = fields.Float(string='Loan Amount')
    installment_count=fields.Integer(string='Installment Count')
    start_date=fields.Datetime(string='Start Date')
    state = fields.Selection(selection=[('draft','Draft'),('approved','Approved'),('ongoing','Ongoing'),('paid','Paid')],string='State',default='draft')
    loan_line_ids=fields.One2many('employee.loan.line','loan_id',string='Loan Lines')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name','New')=='New':
                val['name']=self.env['ir.sequence'].next_by_code('employee loan') or 'New'
        return super().create(vals_list)




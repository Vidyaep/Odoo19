from odoo import api, fields, models
from odoo.exceptions import UserError


class ApprovalOrder(models.Model):
    _inherit = 'sale.order'
    approving_person_id = fields.Many2one('res.partner',string='Approving Person')
    approved = fields.Boolean(string='Approved',readonly=True)
    state = fields.Selection(selection_add=[('approved','Approved')])

    def _create_invoices(self, grouped=False, final=False):
        for record in self:
            if not record.approved and record.state != 'approved':
                raise UserError("Approval is needed to create invoices")
        return super()._create_invoices(grouped=grouped, final=final)

    def action_approve(self):
        for record in self:
            user = self.env.user.name
            if user != record.approving_person_id.name :
              if not record.approved:
                 raise UserError("Approval is not done or approving user is not provided")
            else:
                record.approved = True
                record.state = 'approved'
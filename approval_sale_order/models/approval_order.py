from odoo import api, fields, models
from odoo.exceptions import UserError

class ApprovalOrder(models.Model):
    _inherit = 'sale.order'
    approving_person_id = fields.Many2one('res.partner',string='Approving Person')
    approve_status = fields.Boolean(string='Approved',readonly=True)
    state = fields.Selection(selection_add=[('to approve','To Approve'),('sale',),('cancel',)])

    def action_confirm(self):
        """Function to confirm the order - after quotation is confirmed changed the state to 'to approve' then approve button action works"""
        for record in self:
            record.state='to approve'

    def action_approve(self):
        """Function to approve the sale order by the approving person given and only when the user is approving person approve ,the button action works"""
        for record in self:
            user = self.env.user.name
            if user == record.approving_person_id.name:
                  record.approve_status = True
                  record.state = 'sale'
            else:
                  raise UserError("Approval is not done or user given as approving person can only do the approval")
            # print(record.invoice_status)

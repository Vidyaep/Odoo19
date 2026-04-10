from email.policy import default

from odoo import api, fields, models
from odoo.exceptions import UserError

class InventoryTransfer(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('to_validate','To Validate'),('done',)])
    validating_person_id = fields.Many2one('res.users', string='Validating Person')
    validated = fields.Boolean(string='Validated',default=False)

    def action_validate(self):
        for record in self:
            if record.validating_person_id and record.validating_person_id!=self.env.user :
               raise UserError("Only validating person can validate this.")
            record.validated = True
            record.state = 'to_validate'
            record.validating_person_id = self.env.user

    def button_validate(self):
        for record in self:
            if record.picking_type_id.code =="internal":
                if not record.validated:
                   raise UserError("Approval is Required")
                user=self.env.user.name
                if user!='Administrator':
                    raise UserError("Validation by Admin Only")
        return super(InventoryTransfer,self).button_validate()


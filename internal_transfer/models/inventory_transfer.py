from email.policy import default

from odoo import fields, models
from odoo.exceptions import UserError

class InventoryTransfer(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """Function to perform button validation using super function"""
        if not self.env.user.has_group('internal_transfer.group_transfer_user'):
            raise UserError("You do not have the permission to perform this action")
        return super().button_validate()
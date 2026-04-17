from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare


class ApprovalOrder(models.Model):
    _inherit = 'sale.order'
    approving_person_id = fields.Many2one('res.partner',string='Approving Person')
    approve_status = fields.Boolean(string='Approved',readonly=True)
    state = fields.Selection(selection_add=[('to approve','To Approve')])
    order_line = fields.One2many('sale.order.line','order_id',string="Order Lines")

    def _create_invoices(self,grouped=False, final=False):
        global move
        for record in self:
            print(record.invoice_status)
            if record.approve_status:
                print(record.invoice_status)
                move=super()._create_invoices(grouped, final)
        return move

    def action_approve(self):
        for record in self:
            user = self.env.user.name
            if user == record.approving_person_id.name:
                  record.approve_status = True
                  record.state = 'to approve'
            else:
                  raise UserError("Only allotted person can approve")

    # def _compute_qty_to_invoice(self):
    #     """
    #     Compute the quantity to invoice. If the invoice policy is order, the quantity to invoice is
    #     calculated from the ordered quantity. Otherwise, the quantity delivered is used.
    #     For combo product lines, compute the value if a linked combo item line gets recomputed,
    #     and set `qty_to_invoice` only if at least one of its combo item lines is invoiceable.
    #     """
    #     combo_lines = set()
    #     for line in self.order_line:
    #         if line.state == 'to approve' and not line.display_type:
    #             if line.product_id.type == 'combo':
    #                 combo_lines.add(line)
    #             elif line.product_id.invoice_policy == 'order':
    #                 line.qty_to_invoice = line.product_uom_qty - line.qty_invoiced
    #             else:
    #                 line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
    #             if line.combo_item_id and line.linked_line_id:
    #                 combo_lines.add(line.linked_line_id)
    #         else:
    #             line.qty_to_invoice = 0
    #     for combo_line in combo_lines:
    #         if any(
    #                 line.combo_item_id and line.qty_to_invoice
    #                 for line in combo_line.linked_line_ids
    #         ):
    #             combo_line.qty_to_invoice = combo_line.product_uom_qty - combo_line.qty_invoiced
    #         else:
    #             combo_line.qty_to_invoice = 0

    # @api.depends('state')
    # def _compute_invoice_status(self):
    #     """
    #     Compute the invoice status of a SO line. Possible statuses:
    #     - no: if the SO is not in status 'sale', we consider that there is nothing to
    #       invoice. This is also the default value if the conditions of no other status is met.
    #     - to invoice: we refer to the quantity to invoice of the line. Refer to method
    #       `_compute_qty_to_invoice()` for more information on how this quantity is calculated.
    #     - upselling: this is possible only for a product invoiced on ordered quantities for which
    #       we delivered more than expected. The could arise if, for example, a project took more
    #       time than expected but we decided not to invoice the extra cost to the client. This
    #       occurs only in state 'sale', the upselling opportunity is removed from the list.
    #     - invoiced: the quantity invoiced is larger or equal to the quantity ordered.
    #     """
    #     precision = self.env['decimal.precision'].precision_get('Product Unit')
    #     for line in self.order_line:
    #         if line.state != 'to approve':
    #             line.invoice_status = 'no'
    #         elif line.is_downpayment and line.untaxed_amount_to_invoice == 0:
    #             line.invoice_status = 'invoiced'
    #         elif not float_is_zero(line.qty_to_invoice, precision_digits=precision):
    #             line.invoice_status = 'to invoice'
    #         elif line.state == 'sale' and line.product_id.invoice_policy == 'order' and \
    #                 line.product_uom_qty >= 0.0 and \
    #                 float_compare(line.qty_delivered, line.product_uom_qty, precision_digits=precision) == 1:
    #             line.invoice_status = 'upselling'
    #         elif float_compare(line.qty_invoiced, line.product_uom_qty, precision_digits=precision) >= 0:
    #             line.invoice_status = 'invoiced'
    #         else:
    #             line.invoice_status = 'no'

    # def action_confirm(self):
    #     for record in self:
    #         record.state='to approve'



        # for record in self:for record in self:
        #     user = self.env.user.name
        #     if user == record.approving_person_id.name:
        #         record.approved = True
        #         record.state = 'approved'
        #         print(record.invoice_status)
        #     else:
        #          raise UserError("Approval is not done or approving user is not provided")
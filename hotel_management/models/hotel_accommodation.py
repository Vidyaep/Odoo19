from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, Command
from odoo.exceptions import UserError, ValidationError
from odoo.orm.decorators import ondelete


class HotelAccommodation(models.Model):
    _name = 'hotel.accommodation'
    _description = 'Hotel Accommodation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sequence'
    _order = 'check_in desc'

    sequence = fields.Char("Reference", copy=False, readonly=True, tracking=True, default='New')
    guests = fields.Many2one('res.partner', string="Guests")
    guest_address = fields.Many2one('res.partner', compute="_compute_address", string="Guest Address")
    guest_count = fields.Integer(string="Guest Count", default=1)
    expected_days = fields.Integer(string="Expected Days", default=1)
    expected_date = fields.Date(string="Expected Date", compute='_compute_expected_date', store=True)
    check_in = fields.Datetime(string="Check In", readonly=True)
    check_out = fields.Datetime(string="Check Out", readonly=True)
    bed_type = fields.Selection(string="Beds",
                                selection=[('single', 'Single'), ('double', 'Double'), ('dormitory', 'Dormitory')])

    facility = fields.Many2many('hotel.facility', string="Facility")
    room = fields.Many2many('hotel.room', string="Room")
    status = fields.Selection(readonly=True, default='draft', tracking=True, required=True,
                              selection=[('draft', 'Draft'), ('check-in', 'Check-in'),('check-out', 'Check-out'), ('cancel', 'Cancel')], string="Status")

    id_proof = fields.Char(string="Proof")
    guest_ids = fields.One2many('hotel.guest', 'guest_id', string="Guests")
    order_ids = fields.One2many('hotel.order', 'accommodation_id', string="Order",domain="[('state','=','confirmed')]",ondelete='cascade')
    order_line_ids = fields.Many2many('hotel.order.list', string="Order Lines", compute='_compute_order',domain="[('state','=','confirmed')]",ondelete='cascade')

    total_rent = fields.Float(string="Total Rent", compute='_compute_total_rent')
    total_all = fields.Float(string="Total", compute='_compute_total_all')
    invoice_id = fields.Many2one('account.move', string="Invoice")
    payment_state = fields.Selection(related='invoice_id.payment_state', store=True)
    order_count = fields.Integer(string="Orders", compute='compute_order_count')
    invoice_count = fields.Integer(string="Invoice Count", compute="compute_invoice_count")
    rent_id = fields.Many2one('product.product', string="Rent")
    expense_id = fields.Many2one('product.product', string="Restaurant Expense")
    payment_id = fields.Many2one('hotel.payment', string="Payment",compute='product_payment')
    payment_line_ids = fields.One2many(related='payment_id.payment_line_ids', string="Payment Lines")


    @api.depends('invoice_id')
    def compute_invoice_count(self):
        """Function to calculate invoice count"""
        for record in self:
            record.invoice_count = len(record.invoice_id)

    @api.depends('order_ids')
    def compute_order_count(self):
        """Function to calculate order count"""
        for record in self:
            record.order_count = self.env['hotel.order'].search_count([('accommodation_id', '=', record.id)])

    @api.model_create_multi
    def create(self, vals_list):
        """Function to create accommodation sequence"""
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('accommodation') or 'New'
        return super().create(vals_list)

    def checkin(self):
        """Function to perform operations while checkin"""
        for record in self:
            if record.status == 'check-out':
                raise UserError('Already checked out')
            if record.guest_count > (len(record.guest_ids) + 1):
                raise UserError('Guest Count is higher than registered guests')
            if record.message_attachment_count < 1:
                raise UserError('Please attach documents to the chatter.')

            record.status = 'check-in'
            record.check_in = fields.Datetime.now()
            record.room.write({'state': 'not_available'})
            record.write({'rent_id': record.room.rent})

    def checkout(self):
        """Function to perform operations while checkout"""
        for record in self:
            if record.status == 'check-in':
               record.status = 'check-out'
               record.check_out = fields.Datetime.now()
               record.room.write({'state': 'available'})
            else:
               raise UserError('Check in before checking out')
            all_orders = record.order_ids.ids
            if record.id in all_orders:
                order_index = all_orders.index(record.id) + 1
                record.display_name = f"Restaurant Order {order_index}"
            lines=[]
            lines.append(Command.create({
                            'product_id': self.rent_id.id,
                            'quantity': 1,
                            'price_unit': record.total_rent,
                            'name': 'Room Rent',
                        }))
            count=0
            for order in record.order_ids:
                if order.state == 'confirmed':
                   count+=1
                   lines.append(Command.create({
                    'product_id': self.expense_id.id,
                    'quantity': 1,
                    'price_unit': order.total,
                    'name': 'Restaurant Expense {}'.format(count),
                  }))
            invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': self.guests.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids':lines,
                })
            record.invoice_id = invoice.id
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'view_mode': 'form',
                    'res_id': invoice.id,
                    "target": "current",
                }

    def cancel(self):
        for record in self:
            record.status = 'cancel'

    @api.depends('expected_days')
    def _compute_expected_date(self):
        """Function to calculate expected date"""
        for record in self:
            record.expected_date = fields.Date.today() + relativedelta(days=record.expected_days)

    @api.depends('guests')
    def _compute_address(self):
        """Function to get guest address"""
        for record in self:
            record.guest_address = record.guests.id if record.guests else False

    @api.depends('order_ids.order_line_ids')
    def _compute_order(self):
        """Function to get order lines"""
        for record in self:
            record.order_line_ids = record.order_ids.mapped('order_line_ids')

    @api.depends('room.rent')
    def _compute_total_rent(self):
        """Function to calculate total rent"""
        for record in self:
            days=0
            if record.check_in and record.check_out:
                days = (record.check_out - record.check_in).days
                total = max(days, 1) * sum(record.room.mapped('rent'))
                record.total_rent = total
            else:
                record.total_rent = record.room.rent

    @api.depends('total_rent', 'order_ids.total')
    def _compute_total_all(self):
        """Function to calculate total of rent and restaurant expenses"""
        for record in self:
            total_orders = 0
            for order in record.order_ids:
                if order.state == 'confirmed':
                   total_orders = sum(order.mapped('total'))
        record.total_all = total_orders + record.total_rent

    def action_get_orders(self):
        """Function to get orders for smart tab"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'list,form',
            'res_model': 'hotel.order',
            'domain': [('accommodation_id', '=', self.id)],
            'context': "{'default_accommodation_id': %s}" % self.id,
        }

    def action_view_invoices(self):
        """Function to get invoices for smart tab"""
        self.ensure_one()
        return {
            "name": "Invoices",
            "type": "ir.actions.act_window",
            "view_mode": "list,form",
            "res_model": "account.move",
            "domain": [("id", "in", self.invoice_id.ids)],
            "context": {'default_move_type': 'out_invoice'}
        }

    @api.depends('room', 'order_ids', 'order_line_ids')
    def product_payment(self):
       """Function to get payment lines"""
       for record in self:
         self.ensure_one()
         line = []
         lines = []
         if record.room:
            line.append(Command.create({
                'name': f"Room Rent",
                'quantity': 1,
                'price': record.total_rent,
            }))
         count = 0
         for order in record.order_ids:
             if order.state == 'confirmed':
                 count+=1
                 lines.append(Command.create({
                      'name': f"Restaurant Expense {count}",
                      'quantity': 1,
                      'price': order.total
                 }))
         payment_lines = line + lines
         if line or (lines and record.order_ids.state == 'confirmed'):
            new_payment = self.env['hotel.payment'].create({
                'payment_line_ids': payment_lines
            })
            record.payment_id = new_payment.id
         else:
            record.payment_id = False

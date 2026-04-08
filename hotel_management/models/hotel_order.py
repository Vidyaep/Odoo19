import datetime
from email.policy import default

from odoo import api, fields, models ,Command
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import UserError, ValidationError
from odoo.orm.decorators import ondelete


class HotelOrder(models.Model):
    _name = 'hotel.order'
    accommodation_id = fields.Many2one('hotel.accommodation',string="Accommodation",ondelete='cascade')
    room_id = fields.Many2many(related='accommodation_id.room',string="Room")
    guests=fields.Char(string="Guests",compute='compute_guests')
    order_date=fields.Datetime(string="Order Date",compute="compute_order_date")
    category_id=fields.Many2many('hotel.category',string="Category",store=True)
    quantity=fields.Integer(string="Quantity",store=True)
    item_ids=fields.One2many('hotel.item','item',string="Items",store=True,ondelete='cascade')
    price=fields.Float(string="Price",store=True)
    subtotal=fields.Float(string="Subtotal")
    total=fields.Float(string="Total",compute='compute_total')
    description=fields.Char(string="Description",store=True)
    order_line_ids = fields.One2many('hotel.order.list', 'order_id',string="Order Lines",ondelete='cascade')
    state = fields.Selection(selection=[('draft','Draft'),('received','Received'),('confirmed','Confirmed'),('cancelled','Cancelled')],string="State",default='draft')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    @api.onchange('order_date')
    def compute_order_date(self):
        """Function to compute order date"""
        self.order_date=fields.Datetime.now()

    @api.depends('accommodation_id')
    def compute_guests(self):
        """Function to compute guests based on accommodation"""
        for record in self:
            record.guests = ""
            if record.accommodation_id:
                   first_guest=record.accommodation_id.guests.display_name
                   if record.accommodation_id.guest_count>1:
                      other_guest=record.accommodation_id.guest_ids.mapped('name.name')
                      other_guests_list = ", ".join(other_guest)
                      record.write({'guests': f"{first_guest}, {other_guests_list}"})
                   else:
                      record.guests=first_guest

    @api.onchange('category_id')
    def compute_category_id(self):
        """Function to compute category id for searching"""
        for record in self:
            record.item_ids= self.env['hotel.item'].search([('category','=',record.category_id.ids)])

    @api.depends('order_line_ids.subtotal')
    def compute_total(self):
        """Function to compute total amount of order lines"""
        for record in self:
             record.total = sum(record.order_line_ids.mapped('subtotal'))

    def order_confirm(self):
        """Function to perform operations when order confirmed"""
        for record in self:
            if record.order_line_ids:
                record.state = 'confirmed'

    def order_cancel(self):
        """Function to perform operations when order cancelled"""
        self.state = 'cancelled'



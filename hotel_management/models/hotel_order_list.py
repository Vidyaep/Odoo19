from odoo import fields,models,api
class HotelOrderList(models.Model):
   _name = "hotel.order.list"
   order_id = fields.Many2one('hotel.order',string="Order",ondelete='cascade')
   item_ids = fields.Many2one('hotel.item',string="Items",ondelete='cascade')
   item_name= fields.Char(string="Item Name",readonly=True)
   price = fields.Float(string="Price",readonly=True)
   description= fields.Char(string="Description",readonly=True)
   currency_id= fields.Many2one('res.currency',string="Currency")
   subtotal= fields.Float(string="Subtotal",compute="compute_subtotal",store=True)
   quantity= fields.Float(string="Quantity",readonly=True)
   total= fields.Monetary(string="Total",store=True)

   @api.depends('price', 'quantity')
   def compute_subtotal(self):
      """Function to calculate subtotal"""
      for record in self:
         record.subtotal = record.price * record.quantity


from odoo import fields,models
class HotelKanban(models.TransientModel):
   _name = "hotel.kanban"
   item_ids = fields.Many2one('hotel.item',string="Items")
   order_ids = fields.Many2one('hotel.order',string="Orders")
   item_name = fields.Char(string="Item Name")
   item_quantity = fields.Integer(string="Quantity")
   price = fields.Float(string="Price")
   description = fields.Char(string="Description")

   def add_list(self):
      """Function to add items to list"""
      self.env['hotel.order.list'].create({
         'order_id': self.order_ids.id,
         'item_name': self.item_name,
         'quantity': self.item_quantity,
         'price': self.price,
         'description': self.description,
      })
      self.order_ids.state='received'
      return {'type': 'ir.actions.act_window_close'}
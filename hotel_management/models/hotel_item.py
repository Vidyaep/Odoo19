from odoo import fields, models

class HotelItem(models.Model):
    _name = 'hotel.item'
    _rec_name = 'item_name'
    item_name = fields.Char(string="Food Item Name")
    image=fields.Image(string="Image")
    item=fields.Char(string="Item Name")
    category=fields.Many2one('hotel.category',string="Category")
    currency_id=fields.Many2one('res.currency',string="Currency")
    price=fields.Monetary(string="Price",currency_field="currency_id")
    quantity=fields.Integer(string="Quantity")
    description=fields.Char(string="Description")

    def action_order_kanban_wizard(self):
        """Function to add items to kanban wizard"""
        self.ensure_one()
        order_id= self.env.context.get('default_order_id')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Order Food Item',
            'res_model': 'hotel.kanban',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_ids': order_id,
                'default_item_name': self.item_name,
                'default_image': self.image,
                'default_price': self.price,
                'default_description': self.description,
            },
        }
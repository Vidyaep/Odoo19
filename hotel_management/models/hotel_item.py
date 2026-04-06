from odoo import fields, models
from odoo.addons.test_convert.tests.test_env import record


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
    supplier_id =fields.Many2one('lunch.supplier',string="Supplier")
    product_id=fields.Many2one('lunch.product',string="Product")

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

    def action_lunch(self):
        """Function to add items to lunch wizard"""
        for record in self:
           if record.category:
              categ = self.env['lunch.product.category'].search([('name', '=', record.category.name)])
              if categ:
                 cat_id= categ
              else:
                  category_new = self.env['lunch.product.category'].create({
                      'name':record.category.name,
                  })
                  cat_id = category_new

              item =self.env['lunch.product'].create({
                'name': record.item_name,
                'description': record.description,
                'price': record.price,
                'category_id': cat_id.id,
                'image_1920': record.image,
                'supplier_id': record.supplier_id.id,
              })
              record.product_id = item.id
from odoo import api, fields, models
class AverageCost(models.Model):
    _inherit = 'product.product'

    average_cost = fields.Float(string='Average Cost',compute='_compute_average_cost')

    @api.model
    def _compute_average_cost(self):
        records = self.search([])
        global average_cost
        for record in records:
            products=record.env['purchase.order.line'].search([('product_id','=',record.id),('state','=','purchase')])
            average_cost = 0
            if products:
               total_amount = sum(products.mapped('price_subtotal'))
               total_quantity = sum(products.mapped('product_uom_qty'))
               average_cost=total_amount/total_quantity
            record.write({'average_cost':average_cost})
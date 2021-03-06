# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2014 Agile Business Group (http://www.agilebg.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import fields, models, api


class StockPickingCarriageCondition(models.Model):

    _name = "stock.picking.carriage_condition"
    _description = "Carriage Condition"

    name = fields.Char(string='Carriage Condition', required=True)
    note = fields.Text(string='Note')


class StockPickingGoodsDescription(models.Model):

    _name = 'stock.picking.goods_description'
    _description = "Description of Goods"

    name = fields.Char(string='Description of Goods', required=True)
    note = fields.Text(string='Note')


class StockPickingTransportationReason(models.Model):

    _name = 'stock.picking.transportation_reason'
    _description = 'Reason for Transportation'

    name = fields.Char(string='Reason For Transportation', required=True)
    note = fields.Text(string='Note')


class StockPickingTransportationMethod(models.Model):

    _name = 'stock.picking.transportation_method'
    _description = 'Method of Transportation'

    name = fields.Char(string='Method of Transportation', required=True)
    note = fields.Text(string='Note')


class StockDdT(models.Model):

    _name = 'stock.ddt'
    _description = 'DdT'

    @api.multi
    def get_sequence(self):
        # XXX: allow config of default seq per company
        return self.env['ir.sequence'].search(
            [('code', '=', 'stock.ddt')])[0].id

    name = fields.Char(string='Number')
    date = fields.Datetime(required=True, default=fields.Datetime.now)
    delivery_date = fields.Datetime()
    sequence = fields.Many2one(
        'ir.sequence', string='Sequence',
        default=get_sequence, required=True)
    picking_ids = fields.One2many(
        'stock.picking', 'ddt_id', string='Pickings', readonly=True)
    ddt_lines = fields.One2many(
        'stock.move', 'ddt_id', string='DdT Line', readonly=True,
        compute='_get_lines')
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    delivery_address_id = fields.Many2one(
        'res.partner', string='Delivery Address', required=False)
    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', 'Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description', 'Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        'Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        'Method of Transportation')
    carrier_id = fields.Many2one(
        'delivery.carrier', string='Carrier')
    parcels = fields.Integer()
    note = fields.Text('Note')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('cancelled', 'Cancelled')],
        string='State',
        default='draft'
    )

    def _get_lines(self):
        for ddt in self:
            for picking in ddt.picking_ids:
                ddt.ddt_lines |= picking.move_lines

    @api.multi
    def set_number(self):
        for ddt in self:
            if not ddt.name:
                ddt.write({
                    'name': ddt.sequence.get(ddt.sequence.code),
                })

    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @api.multi
    def action_reopen(self):
        self.write({'state': 'draft'})
        self.delete_workflow()
        self.create_workflow()
        return True

    @api.multi
    def name_get(self):
        result = []
        for ddt in self:
            result.append((ddt.id, "%s" % (ddt.name or 'N/A')))
        return result


class StockPicking(models.Model):

    _inherit = "stock.picking"

    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', string='Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description', string='Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Method of Transportation')
    parcels = fields.Integer()
    ddt_id = fields.Many2one('stock.ddt', string='DdT')
    ddt_type = fields.Selection(
        string="DdT Type", related='picking_type_id.code')

    def action_invoice_create(
            self, cr, uid, ids, journal_id, group=False, type='out_invoice',
            context=None):
        if not context:
            context = {}
        invoice_obj = self.pool['account.invoice']
        
        ctx = {}
        if context:
            for item in context.items():
                ctx[item[0]] = item[1]

        cr.execute('''
                        SELECT MAX(carriage_condition_id), MAX(goods_description_id), MAX(transportation_reason_id), MAX(transportation_method_id)
                        FROM stock_picking
                        WHERE id IN %s
                    ''',(tuple(ids),))
        qry_result = cr.fetchall()
        if qry_result:                               
            ctx.update({'carriage_condition_id': qry_result[0][0],
                        'goods_description_id': qry_result[0][1],
                        'transportation_reason_id': qry_result[0][2],
                        'transportation_method_id': qry_result[0][3],})
        res = super(StockPicking, self).action_invoice_create(cr, uid, ids, journal_id, group, type, context=ctx)

        return res

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        if context is None:
            context = {}
        res = super(StockPicking, self)._get_invoice_vals(cr,uid,key,inv_type,journal_id,move,context=context)
        if res:
            res.update({
                        'carriage_condition_id': context.get('carriage_condition_id', False),
                        'goods_description_id': context.get('goods_description_id', False),
                        'transportation_reason_id': context.get('transportation_reason_id', False),
                        'transportation_method_id': context.get('transportation_method_id', False),
                        })
            if context.get('payment_term'):
                 res.update({
                        'payment_term': context.get('payment_term', False),}
                 )
        return res

class StockMove(models.Model):
    _inherit = "stock.move"

    ddt_id = fields.Many2one('stock.ddt', ondelete="set null")

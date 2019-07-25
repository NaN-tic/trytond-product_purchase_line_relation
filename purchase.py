# This file is part product_purchase_line_relation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PurchaseLine']


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'
    shipment_state = fields.Function(fields.Selection(
        [('none','None'), ('waiting', 'Waiting'),('exception', 'Exception'),
            ('received', 'Received')],'Shipment State'),
            'get_shipment_state', searcher='search_shipment_state')

    @classmethod
    def get_shipment_state(cls, lines, name):
        result = {}.fromkeys([x.id for x in lines])
        for line in lines:
            result[line.id] = 'waiting'
            if line.move_exception:
                result[line.id] = 'exception'
            elif line.purchase == None:
                result[line.id] = 'none'
            elif line.move_done:
                result[line.id] = 'received'
        return result

    @classmethod
    def search_shipment_state(cls, name, clause):
        n,op, state = clause
        lines = cls.search([('purchase.shipment_state', op, state)])
        if state == 'sent':
            partial = cls.search([('purchase.shipment_state', op , 'received')])
            lines += [x for x in partial if x.move_done]

        if state == 'waiting':
            lines = [x for x in lines if not x.move_done]

        if state == None:
            without_purchase = cls.search([('purchase', '=', None)])
            lines += [x for x in without_purchase]
        return [('id', 'in', [x.id for x in lines])]

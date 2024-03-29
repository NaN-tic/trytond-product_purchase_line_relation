from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval


class PurchaseLine(metaclass=PoolMeta):
    'Purchase Line'
    __name__ = 'purchase.line'
    party = fields.Function(fields.Many2One('party.party',
            'Party', context={
            'company': Eval('company', -1),
            }, depends=['company']), 'get_party', searcher='search_party')

    def get_party(self, name):
        return self.purchase.party.id

    @classmethod
    def search_party(cls, name, clause):
        return [('purchase.party',) + tuple(clause[1:])]

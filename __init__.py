# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool


def register():
    Pool.register(
        module='product_purchase_line_relation', type_='model')

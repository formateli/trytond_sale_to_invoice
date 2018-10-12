# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta

__all__ = ['Sale']


class Sale:
    __metaclass__ = PoolMeta
    __name__ = 'sale.sale'

    @classmethod
    def process(cls, sales):
        super(Sale, cls).process(sales)
        Invoice = Pool().get('account.invoice')
        Shipment = Pool().get('stock.shipment.out')
        invoices = []
        for sale in sales:
            if sale.invoice_method != 'order' or \
                    sale.shipment_method != 'order':
                continue
            if sale.state != 'processing':
                continue
            if sale.shipments:
                if len(sale.shipments) > 1:
                    continue
                for ship in sale.shipments:
                    if ship.__class__.__name__ != 'stock.shipment.out':
                        continue
                    if ship.state != 'waiting':
                        continue
                    Shipment.assign([ship,])
                    Shipment.assign([ship,])
                    Shipment.pack([ship,])
                    Shipment.done([ship,])

            for inv in sale.invoices:
                if inv.state == 'draft':
                    inv.invoice_date = sale.sale_date
                    inv.save()
                    invoices.append(inv)

        if invoices:
            Invoice.post(invoices)

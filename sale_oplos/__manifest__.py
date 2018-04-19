# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Oplos',
    'version': '1.0',
    'author': 'Davidsetiyadi@gmail.com',
    'category': 'Custom Development',
    'summary': 'Sale Orders Custom',
    'description': """
    Sales Oplos
""",
    'website': '',
    'depends': ['sale','sale_stock','stock','vit_efaktur'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_views.xml',
        'views/account_views.xml',
        'views/stock_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
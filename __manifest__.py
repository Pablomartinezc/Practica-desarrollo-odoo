# -*- coding: utf-8 -*-
{
    'name': "My Supermarket",  # Module title
    'summary': "Manage products easily",  # Module subtitle phrase
    'description': """
Manage Supermarket
==============
Description related to supermarket.
    """,  # Supports reStructuredText(RST) format
    'author': "Luis Bres Conesa",
    'website': "http://www.example.com",
    'category': 'Tools',
    'version': '14.0.1',
    'depends': ['base'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/supermarket_product.xml',
        'views/supermarket_product_categ.xml',
        #'views/partner.xml',
        'reports/products_report.xml',
        # Si no carga demo data, este siempre carga
        'demo/demo.xml'              
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,    
}

# -*- coding: utf-8 -*-
{
    'name': "Import Product From URL",

    'summary': """
        Import Images Product From URL
    """,
    "license": "LGPL-3",
    'description': """
        Import Images Product From URL
    """,

    'author': "Arman Nur Hidayat",
    'website': "http://www.syntaxdev.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '12.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/import_menu.xml',
    ],
}
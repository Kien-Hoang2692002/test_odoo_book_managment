{
    'name': 'Book Management System',
    'version': '1.0',
    'category': 'Management',
    'summary': 'Module for managing book in library',
    'description': """
        This module helps library to manage book information.
    """,
    'author': 'Kiên Hoàng',
    'depends': ['base', 'mail', 'calendar', 'web'],
    'data': [
        'security/book_security.xml',
        'security/ir.model.access.csv',
        'wizards/publisher_create.xml',
        'views/book_views.xml',
        'views/author_views.xml',
        'views/category_views.xml',
        'views/publisher_views.xml',
        'views/rental_views.xml',
        'report/report_book_rental.xml',
        'views/invoice_views.xml',
        'views/res_customer_views.xml',
        'views/menu_views.xml',
        'data/book_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/book_managment/static/src/css/custom_kanban.css',
        ],
    },
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

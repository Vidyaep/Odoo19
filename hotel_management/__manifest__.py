{
    'name': "Hotel Management",
    'version': '1.0',
    'depends': ['base','mail','account','product'],
    'author': "Author Name",
    'license':"",
    'category': 'Hotel Management',
    'sequence':-20,
    'description': """
    Description text
    """,
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'data/hotel_management_data.xml',
        'data/hotel_management_sequence.xml',
        'views/hotel_room_views.xml',
        'views/hotel_facility_views.xml',
        'views/hotel_item_views.xml',
        'views/hotel_category_views.xml',
        'views/hotel_accommodation_views.xml',
        'views/hotel_order_views.xml',
        'views/hotel_kanban_views.xml',
        'views/hotel_guest_views.xml',
        'views/hotel_management_menus.xml',
    ],
}
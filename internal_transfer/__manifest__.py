{
    'name': "Internal Transfer",
    'version': '1.0',
    'depends': ['base','stock'],
    'author': "Author Name",
    'license':"",
    'category': 'Internal Transfer',
    'sequence':-20,
    'description': """
    Description text
    """,
    'application': True,
    'installable': True,
    'data': [
        'security/internal_transfer_groups.xml',
        'security/ir.model.access.csv',
    ],
}
{
    'name': "Employee Loan",
    'version': '19.0.1.0.0',
    'depends': ['base','hr'],
    'author': "Author Name",
    'category': 'Employee Loan',
    'sequence':-20,
    'description': """
    Description text
    """,
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'data/employee_loan_sequence.xml',
        'views/employee_loan_views.xml',
        'views/employee_loan_line_views.xml',
        'views/employee_loan_menus.xml'
        ]
}


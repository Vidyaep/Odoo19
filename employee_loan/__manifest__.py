{
    'name': "Employee Loan",
    'version': '1.0',
    'depends': ['base'],
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
        'views/employee_loan.xml',
        'views/employee_loan_views.xml',
        'views/employee_loan_menus.xml'
        ]
}


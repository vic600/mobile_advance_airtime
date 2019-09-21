# -*- coding: utf-8 -*-
{
    'name': "Mobile airtime ",
    'summary': "Allows airtime  for employeese",
    'description': """
        This plugin can be used to issue airtime. 
	
    """,
    'author': "vic",
    'version': '10.0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/mobile_airtime.xml',
    ],
    'installable': True,
    'auto_install': False,
}

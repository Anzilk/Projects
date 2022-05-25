# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "Purchase Advance Payment",
    'version': '15.0.1.0.0',
    'description': """Purchase Advance Payment""",
    'summary': """ Advance Payment options for purchase""",
    'author': "Cybrosys Techno Solutions",
    'website': "https://www.cybrosys.com",
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'depends': ['base', 'purchase', 'account', 'stock'],
    'category': 'Purchase',
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_advance_payment_views.xml',
        'views/res_config_settings_views.xml',
        'views/purchase_views.xml'],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'auto_install': False,
    'application': False,

}

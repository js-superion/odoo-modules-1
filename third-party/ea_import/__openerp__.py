# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Enapps LTD (<http://www.enapps.co.uk>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Enapps Import Data tool',
    'version': '18',
    'depends': [
        'base',
    ],
    'author': 'ENAPPS LTD',
    'description': '''Import and export csv files''',
    'website': 'http://www.enapps.co.uk/',
    'category': 'Tool',
    'demo': [
    ],

    'data':  [
                    'security/security_groups.xml',
                    'security/ir.model.access.csv',
                    'ea_import_template_view.xml',
                    'ea_import_template_line_view.xml',
                    'ea_import_template_line_calc_field_view.xml',
                    'ea_import_template_line_boolean_field_view.xml',
                    'ea_import_template_line_regexp_field_view.xml',
                    'ea_import_chain_view.xml',
                    'ea_import_chain_result_view.xml',
                    'ea_import_log_view.xml',
                    'ea_import_scheduler.xml',
                    'ea_import_scheduler_data.xml',
                    'ea_export_config_view.xml',
                    'wizard/import_wizard_view.xml',
                    'configs/mysql_config_view.xml',
                    'configs/ftp_config_view.xml',
                    'data/update_templates.xml',
                    ],
    'active': False,
    'application': True,
    'installable': True,
    'images': ['images/chain_form.png', 'images/template_form.png'],
    'external_dependencies': {
                            'python': ['MySQLdb']  # On Linux can be installed using 'apt-get install python-mysqldb'
                            }

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

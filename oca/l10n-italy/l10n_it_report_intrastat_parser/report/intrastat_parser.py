# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Associzione Odoo Italia
#    All Rights Reserved
#    Andrea Cometa <a.cometa@apuliasoftware.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp.report import report_sxw
from openerp import api, models
from openerp.http import request


class ReportIntrastatQweb(models.AbstractModel):

    _name = 'report.l10n_it_report_intrastat.report_intrastat_mod1'
                                             
    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'l10n_it_report_intrastat.report_intrastat_mod1')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'objects': self.env[report.model].browse(self._ids),
        }
        # print docargs
        return report_obj.render(
            'l10n_it_report_intrastat.report_intrastat_mod1',
            docargs)

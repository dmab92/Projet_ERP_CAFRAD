# See LICENSE file for full copyright and licensing details.

import datetime
from odoo import models, fields, api
from datetime import datetime

class report_time_table_cafrad(models.AbstractModel):
    _name = 'report.cafrad_app.timetable_report'
    _description = "Report Timetable"

    def _get_timetable(self, timetable_id):
        timetable_detail = []
        self._cr.execute('''select t.start_time,t.end_time,s.name,week_day,
                        st.employee_id, hr.name as
                        teacher from time_table_line_cafrad t,
                        matiere_cafrad s, resource_resource r, teacher_cafrad
                        st, hr_employee
                        hr where t.matiere_id= s.id and t.teacher_id=st.id and
                        st.employee_id= hr.id
                        and  t.table_id = %s
                        group by start_time,end_time,s.name,week_day,
                        st.employee_id,hr.name
                        order by start_time''', tuple([timetable_id.id]))
        res = self._cr.dictfetchall()
        self._cr.execute('''select start_time,end_time from time_table_line_cafrad
                        where table_id=%s group by start_time,end_time
                        order by start_time''', tuple([timetable_id.id]))
        time_data = self._cr.dictfetchall()
        for time_detail in time_data:
            for data in res:
                if ((time_detail['start_time'] == data['start_time']) and
                        (time_detail['end_time'] == data['end_time'])):
                    if (data['name'] == 'Recess'):
                        time_detail[data['week_day']] = data['name']
                    else:
                        td = data['name'] + '\n(' + data['teacher'] + ')'
                        time_detail[data['week_day']] = td
            timetable_detail.append(time_detail)
        return timetable_detail

    def date_to_literal(self, date):
        month_to_literal = [
            'Janvier',
            'Fevrier',
            'Mars',
            'Avril',
            'Mai',
            'Juin',
            'Juillet',
            'Aout',
            'Septembre',
            'Octobre',
            'Novembre',
            'Decembre',
        ]
        ##        print date
        if isinstance(date, str):
            if len(date) == 10:
                format = '%Y-%m-%d'
            else:
                format = '%Y-%m-%d %H:%M:%S'
        date = datetime.strptime(date, format)
        if not isinstance(date, datetime):
            return ''
        return str(date.day).zfill(2) + ' ' + month_to_literal[date.month - 1] + ' ' + str(date.year)



    @api.model
    def _get_report_values(self, docids, data=None):
        timetable_report = self.env['ir.actions.report']._get_report_from_name('cafrad_app.timetable_report')
        docs = self.env['time.table.cafrad'].browse(docids)
        return {
            'doc_ids': docids,
            'docs': docs,
            'doc_model': timetable_report.model,
            'data': data,
            'get_timetable': self._get_timetable,
            'get_date_to_literal': self.date_to_literal
        }


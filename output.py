# coding: UTF-8
from __future__ import unicode_literals

import math
import latex
import chart
import settings
from overtime.overtime import get_workhours


def console(invoice, date_range=None):
    def hline():
        return '+'.join(['-'*(p_len+1), '-'*(r_len),
                        '-'*(h_len+4), '-'*(w_len+2)])

    if not invoice.projects:
        print('nothing there')
        return

    # header
    head_proj = 'projects'
    head_hours = 'hours'
    head_rate = 'rate'
    head_wage = 'rate*hours'

    # max project name length
    p_len = len(max(invoice.projectnames, key=len))
    p_len = max(p_len, len(head_proj))
    # sum of hours
    h_sum = invoice.sum_hours
    # wage sum
    w_sum = invoice.sum_money
    # max wage len
    w_len = int(math.log10(int(w_sum)))+4
    w_len = max(w_len, len(head_wage))
    # max project hours len
    if int(h_sum) >= 1:
        h_len = int(math.log10(int(h_sum)))+3
    else:
        h_len = 3
    h_len = max(h_len, len(head_hours))
    # width of output
    c_len = p_len+h_len+3

    r_len = len(head_rate)+3
    r_avg = w_sum/h_sum

    # print header
    print(' | '.join([head_proj.ljust(p_len),
                      head_hours.rjust(h_len),
                      head_rate.rjust(r_len),
                      head_wage.rjust(w_len+1)]))
    print(hline())

    # print project information
    for project in invoice:
        proj_rate = project.avg_rate
        print('%s | %s | %s | €%s' % (project.name.ljust(p_len),
              ('%0.2f' % project.sum_hours).rjust(h_len),
              ('%0.2f' % proj_rate).rjust(r_len),
              ('%0.2f' % project.sum_money).rjust(w_len)))

    print(hline())
    # print summary
    print('%s | %s | €%s' % (('%.1f' % h_sum).rjust(c_len),
                              ('%.2f' % r_avg).rjust(r_len),
                              ('%.2f' % w_sum).rjust(w_len)))
    if date_range:
        print(hline())
        overtime_sum = h_sum - get_workhours(*date_range)
        print('%s | %s | %s | €%s' % ('Overtime'.ljust(p_len),
                                 ('%.1f' % overtime_sum).rjust(h_len),
                                 ('%.2f' % r_avg).rjust(r_len),
                                 ('%.2f' % (overtime_sum*r_avg)).rjust(w_len)))


def pdf(invoice):
    # TODO
    return latex.pdflatex(invoice)


def charts(invoice, types=None):
    if types is None:
        types = settings.charts
    c = []
    if 'project_distribution_hours' in types:
        c.append(chart.project_distribution(invoice, 'hours'))
    if 'project_distribution_money' in types:
        c.append(chart.project_distribution(invoice, 'money'))

    return c

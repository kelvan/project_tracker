#!/usr/bin/python

import sys
import os
from os.path import dirname, join
import subprocess
from datetime import date, datetime
import argparse
import math
import re

from input import load_from_csv
import output
import defaults
from invoice import *
from settings import *
from project_settings import PROJECTS

parser = argparse.ArgumentParser(description='Get overview of your projects '
                                 'and generate invoices')
parser.add_argument(metavar='filename', help='specify input timesheet',
                    dest='inputfile')
group = parser.add_mutually_exclusive_group()
date_group = group.add_argument_group('Date filter')
date_group.add_argument('-m', metavar='month', help='filter by month',
                        default=None, dest='month', type=int)
date_group.add_argument('-y', metavar='year', help='filter by year',
                        default=None, dest='year', type=int)
date_group.add_argument('-d', metavar='day', help='filter by day',
                        default=None, dest='day', type=int)
# TODO Today invalid with day, month, year set
group.add_argument('-t', '--today', action='store_true',
                   help='show today')
parser.add_argument('-p', metavar='project', help='filter by project',
                    default=None, dest='project')
parser.add_argument('-i', '--invoice', action='store_true',
                    help='generate invoice splitted per project')
parser.add_argument('-r', '--round', action="store_true",
                    help='round hours')
parser.add_argument('-u', '--uncleared', action='store_true',
                    help='Show only uncleared hours')
parser.add_argument('-w', '--hourly_rate', type=float,
                    help='overwrite hourly wage rate')
parser.add_argument('-c', '--charts', action='store_true',
                    help='Render charts in browser')

args = parser.parse_args()

hours = {}  # projectname: hours
lst = []

if args.project:
    project = args.project
else:
    project = None

invoicedirectory = join(dirname(__file__), 'invoices')
pdfdir = join(invoicedirectory, 'pdf')
texdir = join(invoicedirectory, 'tex')


def get_invoicenumber(dte):
    dt = datetime.strftime(dte, '%y%m')
    c = sorted(filter(lambda f: re.match(dt+"\d\d.pdf", f),
                      os.listdir(pdfdir)))
    if c:
        inum = int(c[-1][4:-4])+1
    else:
        inum = 1
    return '%s%s' % (dt, str(inum).rjust(2, '0'))

today = date.today()


def project_or_default_settings(project, item):
    if project is None or not project.lower() in PROJECTS:
        return getattr(defaults, item)

    proj_settings = PROJECTS[project.lower()]

    return proj_settings.get(item, getattr(defaults, item, None))


vals = ['address', 'name', 'recipient', 'greeting', 'closing', 'currency',
        'vat', 'iban', 'bic']
settings = {v: project_or_default_settings(project, v) for v in vals}
settings.update(date=today, number=get_invoicenumber(today))

invoice = Invoice(**settings)

today = date.today()

day = None
if args.day:
    day = args.day

# XXX use tuple (from, to) as date range
month = None
if args.month:
    month = args.month
elif day:
    month = today.month
    if day > today.day:
        # XXX should be replaced after building date range
        month = month - 1 if month > 1 else 12

year = None
if args.year:
    if args.year >= 1000:
        year = args.year
    else:
        year = args.year + 2000
elif month:
    year = today.year
    if month > today.month:
        year -= 1

if args.today:
    year, month, day = today.timetuple()[:3]

date_ = [year, month, day]
formatted_date = '-'.join([str(d).zfill(2) for d in date_ if d])
if formatted_date:
    print('Show for: %s' % formatted_date)

rnd = args.round
uncleared = args.uncleared

rate = None
if args.hourly_rate:
    rate = args.hourly_rate

charts = args.charts

# load csv
try:
    lst = load_from_csv(args.inputfile)
except ValueError as e:
    print(e.message)
    sys.exit(1)

for w in lst:
    prj = w['project']

    if prj == 'CLEARED':
        if uncleared:
            hours = {}
            invoice.projects = []
        continue

    if (not year or w['date'].year == year) and \
       (not month or w['date'].month == month) and \
       (not day or w['date'].day == day) and \
       (not project or project.lower() == prj.lower()):

        h = float(w['hours'])

        if prj in hours:
            h += hours[prj]
        hours[prj] = h

if rnd:
    for key, value in hours.items():
        hours[key] = math.ceil(value)

for proj, h in hours.items():
    p = Project(proj)
    if rate is None:
        c_rate = project_or_default_settings(proj, 'rate')
    else:
        c_rate = rate

    p.add_fee(Fee('Development', c_rate, h))
    invoice.add_project(p)

if charts:
    for chart in output.charts(invoice):
        chart.render_in_browser()

if args.invoice:
    pdf = output.pdf(invoice)
    subprocess.call(('xdg-open', pdf))

output.console(invoice)

from datetime import datetime
import csv
import re

DATEPSTR = '%Y-%m-%d'
DATE_REGEX = '^\d{4}-\d{2}-\d{2}$'
FLOAT_REGEX = '^\d*\.\d+$'


def convert_dict(dic):
    for key in dic.keys():
        elem = dic[key]

        if elem is None:
            raise ValueError(u'Missing input: %s in %s' % (key, dic))
        elif re.match(DATE_REGEX, elem):
            dic[key] = datetime.strptime(elem, '%Y-%m-%d').date()
        elif re.match(FLOAT_REGEX, elem):
            dic[key] = float(elem)

    return dic


def load_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        lst = [convert_dict(x) for x in reader]
    return lst

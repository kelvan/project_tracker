import pygal

def project_distribution(invoice, type_='hours'):
    chart = pygal.Pie()
    chart.config.title = 'Project Distribution'
    chart.config.explicit_size = True
    for project in invoice:
        if type_ == 'hours':
            chart.add(project.name, project.sum_hours)
        elif type_ == 'money':
            chart.add(project.name, project.sum_money)

    return chart

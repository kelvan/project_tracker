class Fee():
    def __init__(self, fee_type, rate, hours):
        self.type = fee_type
        self.rate = rate
        self.hours = hours

    def __unicode__(self):
        return "{0}: {1}".format(self.type, self.sum)

    @property
    def sum(self):
        return self.hours * self.rate


class Project():
    def __init__(self, name, fees=None):
        if fees is None:
            self.fees=[]
        else:
            self.fees = fees
        self.name = name

    def __unicode__(self):
        return self.name + ": " + ", ".join(self.fees)

    @property
    def sum_hours(self):
        return sum([f.hours for f in self.fees])

    @property
    def sum_money(self):
        return sum([f.sum for f in self.fees])

    @property
    def avg_rate(self):
        return self.sum_money / self.sum_hours

    def add_fee(self, fee):
        self.fees.append(fee)


class Invoice():
    def __init__(self, address, name, date, number, recipient,
                 greeting, closing, currency, vat, iban, bic, projects=[]):
        self.address = address
        self.name = name
        self.date = date
        self.number = number
        self.recipient = recipient
        self.greeting = greeting
        self.closing = closing
        self.currency = currency
        self.vat = vat
        self.iban = iban
        self.bic = bic
        self.projects = projects

    def __unicode__(self):
        return ", ".join(self.projects)

    def __iter__(self):
        for proj in self.projects:
            yield proj

    @property
    def sum_hours(self):
        return sum([p.sum_hours for p in self.projects])

    @property
    def sum_money(self):
        return sum([p.sum_money for p in self.projects])

    @property
    def projectnames(self):
        return [p.name for p in self.projects]

    def add_project(self, project):
        self.projects.append(project)

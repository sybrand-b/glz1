from datetime import datetime


class FeestDag(object):
    """" for every festival specifies three attributes: the day, it's name, and it's color """

    l_fieldnames = ['dag','benaming','kleur']

    def __init__(self, datum, benaming, kleur='groen'):
        """

        :type self: object
        """
        self.dag = datetime.strptime(datum, '%d-%m-%Y') if isinstance(datum,str) else datum
        self.benaming = benaming
        self.kleur = kleur

    def __repr__(self):
        return "%s,%s,%s" % (self.dag.strftime("%x"), self.benaming, self.kleur)

    def __str__(self):
        return '"%s %s"; "%s"; "Kleur %s"' % (self.dag.strftime("%A").ljust(10), self.dag.strftime("%d-%m-%Y"),
                                       self.benaming.ljust(32), self.kleur)

    def __cmp__(self, other):
        return cmp(self.dag, other.dag)

    def day2list(self):
        return list(repr(self).split(','))

    def day2dict(self):
        return dict(zip(FeestDag.l_fieldnames,self.day2list()))

    def benaming(self):
        return self.benaming

    def kleur(self):
        return self.kleur

    def dag(self):
        return self.dag

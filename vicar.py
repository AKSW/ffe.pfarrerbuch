# -*- coding: utf-8 -*-
"""
Object class for each vicar entry

Author: Robert R.
"""


class Vicar(object):
    name = 'k.A.'
    ordination = 'k.A.'
    birthday = 'k.A.'
    obit = 'k.A.'
    married = 'k.A.'
    father = 'k.A.'
    mother = 'k.A.'
    siblings = ['k.A.']
    offspring = ['k.A.']
    vicars = ['k.A.']
    pastors = ['k.A.']
    institutions = ['k.A.']
    teachers = ['k.A.']
    education = 'k.A.'
    misc = 'k.A.'
    archive = 'k.A.'
    literature = 'k.A.'

    def __init__(self, name, ordination, birthday, obit, married, father,
                    mother, siblings, offspring, vicars, pastors, institutions,
                    teachers, education, misc, archive, literature):
        self.name = name                    # name of the vicar
        self.ordination = ordination        # ordination of the vicar
        self.birthday = birthday            # birthday of the vicar
        self.obit = obit                    # obit of the vicar
        self.married = married              # Wife / Husband of the vicar
        self.father = father                # father of the vicar
        self.mother = mother                # mother of the vicar
        self.siblings = siblings            # siblings of the vicar
        self.offspring = offspring          # the offspring of the vicar
        self.vicars = vicars                # vicars of the vicar
        self.pastors = pastors              # pastors of the vicar
        self.institutions = institutions    # institutions of the vicar
        self.teachers = teachers            # teachers of the vicar
        self.education = education          # the education of the vicar
        self.misc = misc                    # diverse annotations
        self.archive = archive              # archive sources
        self.literature = literature        # used literature

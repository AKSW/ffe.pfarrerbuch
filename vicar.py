# -*- coding: utf-8 -*-
"""
Object class for each vicar entry

Author: Robert R.
"""


class Vicar(object):
    name = 'k.A.'
    birthday = 'k.A.'
    obit = 'k.A.'
    father = 'k.A.'
    mother = 'k.A.'
    ordination = 'k.A.'
    offspring = ['k.A.']
    education = 'k.A.'
    misc = 'k.A.'

    def __init__(self, name, birthday, obit, father, mother, ordination,
                 offspring, education, misc):
        self.name = name                    # name of the vicar
        self.birthday = birthday            # birthday of the vicar
        self.obit = obit                    # obit of the vicar
        self.father = father                # father of the vicar
        self.mother = mother                # mother of the vicar
        self.ordination = ordination        # ordination of the vicar
        self.offspring = offspring          # the offspring of the vicar
        self.education = education          # the education of the vicar
        self.misc = misc                    # diverse stuff

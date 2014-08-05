# -*- coding: utf-8 -*-
"""
Object class for each vicar entry

Author: Robert R.
"""


class Vicar(object):
    id = 0
    name = None             # name of the vicar
    ordination = None       # ordination of the vicar
    birthday = None         # birthday of the vicar
    obit = None             # obit of the vicar
    married = None          # Wife / Husband of the vicar
    father = None           # father of the vicar
    mother = None           # mother of the vicar
    siblings = []           # siblings of the vicar
    offspring = []          # the offspring of the vicar
    vicars = []             # vicars of the vicar
    pastors = []            # pastors of the vicar
    institutions = []       # institutions of the vicar
    teachers = []           # teachers of the vicar
    education = []          # the education of the vicar
    misc = None             # diverse annotations
    archive = None          # archive sources
    literature = None       # used literature

    def __init__(self, id):
        self.id = id

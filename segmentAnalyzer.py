# -*- coding: utf-8 -*-

"""
Class for analyzing a certain segment and creating a corresponding output

Author: Robert R.
"""

from vicar import Vicar
from analyzer import Analyzer
import xml.etree.ElementTree as ElementTree
import datetime
import dateutil.parser

class SegmentAnalyzer:

    def __init__(self, segment, vicar):
        self.segment = segment
        self.vicar = vicar

    def analyze(self):
        for i, line in enumerate(self.segment):
            if i == 0:
                self.vicar.name = line
            else:
                analyzer = Analyzer(line, self.vicar)
                analyzer.analyze()

    def createEntry(self, root):
        self.analyze()
        #self.stripLines()
        entry = ElementTree.SubElement(root, 'vicar')
        ElementTree.SubElement(entry, 'id').text = str(self.vicar.id)
        ElementTree.SubElement(entry, 'name').text = self.vicar.name.strip()
        ordination = ElementTree.SubElement(entry, 'ordination')
        if (self.vicar.ordination != 'k.A.'):
            ordination.text = self.vicar.ordination.strip().split(',')[0]
            if (len(self.vicar.ordination.strip().split(',')) == 2):
                ElementTree.SubElement(ordination, 'date').text = self.parsedate(self.vicar.ordination.strip())
        else:
            ordination.text = 'k.A.'
        birthday = ElementTree.SubElement(entry, 'birthday')
        if (self.vicar.birthday != 'k.A.'):
            birthday.text = self.vicar.birthday.strip().split(',')[0]
            if (len(self.vicar.birthday.strip().split(',')) == 2):
                ElementTree.SubElement(birthday, 'date').text = self.parsedate(self.vicar.birthday.strip())
        else:
            birthday.text = 'k.A.'
        obit = ElementTree.SubElement(entry, 'obit')
        if (self.vicar.obit != 'k.A.'):
            obit.text = self.vicar.obit.strip().split(',')[0]
            if (len(self.vicar.obit.strip().split(',')) == 2):
                ElementTree.SubElement(obit, 'date').text = self.parsedate(self.vicar.obit.strip())
        else:
            obit.text = 'k.A.'
        ElementTree.SubElement(entry, 'father').text = self.vicar.father.strip()
        ElementTree.SubElement(entry, 'mother').text = self.vicar.mother.strip()
        if len(self.vicar.siblings) > 0:
            for sibling in self.vicar.siblings:
                ElementTree.SubElement(entry, 'sibling').text = sibling.strip()
        if len(self.vicar.offspring) > 0:
            for offspring in self.vicar.offspring:
                ElementTree.SubElement(entry, 'offspring').text = offspring.strip()
        if len(self.vicar.vicars) > 0:
            for vicar in self.vicar.vicars:
                ElementTree.SubElement(entry, 'vicar').text = vicar.strip()
        if len(self.vicar.pastors) > 0:
            for pastor in self.vicar.pastors:
                ElementTree.SubElement(entry, 'pastor').text = pastor.strip()
        if len(self.vicar.institutions) > 0:
            for institution in self.vicar.institutions:
                ElementTree.SubElement(entry, 'institution').text = institution.strip()
        if len(self.vicar.teachers) > 0:
            for teacher in self.vicar.teachers:
                ElementTree.SubElement(entry, 'teacher').text = teacher.strip()
        if len(self.vicar.education) > 0:
            for education in self.vicar.education:
                ElementTree.SubElement(entry, 'education').text = education.strip()
        ElementTree.SubElement(entry, 'misc').text = self.vicar.misc.strip()
        ElementTree.SubElement(entry, 'archive').text = self.vicar.archive.strip()
        ElementTree.SubElement(entry, 'literature').text = self.vicar.literature.strip()
        return entry

    def parsedate(self, text):
        defaultDate = datetime.datetime(datetime.MINYEAR, 1, 1)
        date = dateutil.parser.parse(text.replace('.','/'), default = defaultDate, fuzzy = True).strftime('%d.%m.%Y')
        if ("01.01" in date[:5]):
            return date[6:]
        elif ("01" in date[:2]):
            return date[3:]
        else:
            return date
# -*- coding: utf-8 -*-

"""
Class for analyzing a certain segment and creating a corresponding output

Author: Robert R.
"""

from vicar import Vicar
from analyzer import Analyzer
import xml.etree.ElementTree as ElementTree

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
        ElementTree.SubElement(entry, 'name').text = self.vicar.name.strip()
        ElementTree.SubElement(entry, 'ordination').text = self.vicar.ordination.strip()
        ElementTree.SubElement(entry, 'birthday').text = self.vicar.birthday.strip()
        ElementTree.SubElement(entry, 'obit').text = self.vicar.obit.strip()
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


# -*- coding: utf-8 -*-

"""
Class for analyzing a certain segment and creating a corresponding output

Author: Robert R.
"""

from vicar import Vicar
from analyzer import Analyzer
import re
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

    def analyzeName(self, name):
        splitname = ['0'] * 4
        if ('(' not in name):
            splitname[0] = name.split(',')[0]
            splitname[2] = name.split(',')[1]
        elif (name.find(',') < name.find('(')):
            tmp = name.split(',', 1)
            splitname[0] = tmp[0]
            splitname[2] = tmp[1][:tmp[1].find('(')]
            splitname[3] = tmp[1][tmp[1].find('(') + 1:tmp[1].find(')')]
        else:
            tmp = name.split('(', 1)
            splitname[0] = tmp[0]
            splitname[1] = tmp[1][:tmp[1].find(')')]
            if ('(' not in tmp[1]):
                splitname[2] = tmp[1][tmp[1].find(')'):].split(',')[1]
            else:
                tmp2 = tmp[1][tmp[1].find(')'):].split(',', 1)[1]
                splitname[2] = tmp2[:tmp2.find('(')]
                splitname[3] = tmp2[1][tmp2[1].find('(') + 1:tmp2[1].find(')')]
        return splitname

    def parsedate(self, text):
        defaultDate = datetime.datetime(datetime.MINYEAR, 1, 1)
        date = dateutil.parser.parse(text.replace('.', '/'), default=defaultDate, fuzzy=True).strftime('%d.%m.%Y')
        if ("01.01" in date[:5]):
            return date[6:]
        elif ("01" in date[:2]):
            return date[3:]
        else:
            return date

    def analyzeDate(self, text):
        analyzed = ['0'] * 3
        #0 = date
        #1 = date inaccuracy - need proper implementation for now not implemented
        #2 = misc
        if ('(' in text and text.find('(') == text.rfind('(')):
            tmp = text[text.find('(') + 1:text.find(')')]
            if (re.search('\d+-\d+', tmp)):
                analyzed[0] = re.findall('\d+-\d+', tmp)[0]
            elif (re.search('\d+-', tmp)):
                analyzed[0] = re.findall('\d+-', tmp)[0]
            elif (re.search('\d+', tmp)):
                analyzed[0] = re.findall('\d+', tmp)[0]
            else:
                analyzed[2] = tmp
        elif ('(' in text):
            front = text[text.find('(') + 1:text.find(')')]
            back = text[text.rfind('(') + 1:text.rfind(')')]
            if (re.search('\d+', front)):
                analyzed[2] = back
                if (re.search('\d+-\d+', front)):
                    analyzed[0] = re.findall('\d+-\d+', front)[0]
                elif (re.search('\d+-', front)):
                    analyzed[0] = re.findall('\d+-', front)[0]
                elif (re.search('\d+', front)):
                    analyzed[0] = re.findall('\d+', front)[0]
                else:
                    analyzed[2] = analyzed[2] + ', ' + front
            if (re.search('\d+', back)):
                analyzed[2] = front
                if (re.search('\d+-\d+', back)):
                    analyzed[0] = re.findall('\d+-\d+', back)[0]
                elif (re.search('\d+-', back)):
                    analyzed[0] = re.findall('\d+-', back)[0]
                elif (re.search('\d+', back)):
                    analyzed[0] = re.findall('\d+', back)[0]
                else:
                    analyzed[2] = analyzed[2] + ', ' + back
        return analyzed

    # Create the XML tree
    def createEntry(self, root):
        self.analyze()

        #begin with main entry
        entry = ElementTree.SubElement(root, 'vicar')
        ElementTree.SubElement(entry, 'id').text = str(self.vicar.id)

        #name
        name = ElementTree.SubElement(entry, 'name')

        #surname and variations
        ElementTree.SubElement(name, 'surname').text = self.analyzeName(self.vicar.name.strip())[0].strip()
        if(len(self.analyzeName(self.vicar.name.strip())[1]) > 2):
            for variation in self.analyzeName(self.vicar.name.strip())[1].split(','):
                ElementTree.SubElement(name, 'surnameVariation').text = variation.strip()

        #forename and variations
        ElementTree.SubElement(name, 'forename').text = self.analyzeName(self.vicar.name.strip())[2].strip()
        if(len(self.analyzeName(self.vicar.name.strip())[3]) > 2):
            for variation in self.analyzeName(self.vicar.name.strip())[3].split(','):
                ElementTree.SubElement(name, 'forenameVariation').text = variation.strip()

        #ordination
        if (self.vicar.ordination is not None):
            ordination = ElementTree.SubElement(entry, 'ordination')
            ElementTree.SubElement(ordination, 'place').text = self.vicar.ordination.strip().split(',')[0]
            if (len(self.vicar.ordination.strip().split(',')) == 2):
                ElementTree.SubElement(ordination, 'date').text = self.parsedate(self.vicar.ordination.strip())

        #birthday
        if (self.vicar.birthday is not None):
            birthday = ElementTree.SubElement(entry, 'birthday')
            ElementTree.SubElement(birthday, 'place').text = self.vicar.birthday.strip().split(',')[0]
            if (len(self.vicar.birthday.strip().split(',')) == 2):
                ElementTree.SubElement(birthday, 'date').text = self.parsedate(self.vicar.birthday.strip())

        #obit
        if (self.vicar.obit is not None):
            obit = ElementTree.SubElement(entry, 'obit')
            ElementTree.SubElement(obit, 'place').text = self.vicar.obit.strip().split(',')[0]
            if (len(self.vicar.obit.strip().split(',')) == 2):
                ElementTree.SubElement(obit, 'date').text = self.parsedate(self.vicar.obit.strip())

        #Father
        if (self.vicar.father is not None):
            ElementTree.SubElement(entry, 'father').text = self.vicar.father.strip()

        #Mother
        if (self.vicar.mother is not None):
            ElementTree.SubElement(entry, 'mother').text = self.vicar.mother.strip()

        #Siblings
        if len(self.vicar.siblings) > 0:
            for sibling in self.vicar.siblings:
                if ('(' in sibling):
                    siblingEntry = ElementTree.SubElement(entry, 'sibling')
                    ElementTree.SubElement(siblingEntry, 'name').text = sibling[:sibling.find('(')].strip()
                    siblingData = self.analyzeDate(sibling)
                    if (len(siblingData[0]) > 3):
                        ElementTree.SubElement(siblingEntry, 'date').text = siblingData[0].strip()
                    if (len(siblingData[2]) > 2):
                        ElementTree.SubElement(siblingEntry, 'misc').text = siblingData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'sibling').text = sibling.strip()
        del(self.vicar.siblings[:])

        #Offspring
        if len(self.vicar.offspring) > 0:
            for offspring in self.vicar.offspring:
                if ('(' in offspring):
                    offspringEntry = ElementTree.SubElement(entry, 'offspring')
                    ElementTree.SubElement(offspringEntry, 'name').text = offspring[:offspring.find('(')].strip()
                    offspringData = self.analyzeDate(offspring)
                    if (len(offspringData[0]) > 3):
                        ElementTree.SubElement(offspringEntry, 'date').text = offspringData[0].strip()
                    if (len(offspringData[2]) > 2):
                        ElementTree.SubElement(offspringEntry, 'misc').text = offspringData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'offspring').text = offspring.strip()
        del(self.vicar.offspring[:])

        #Vicars
        if len(self.vicar.vicars) > 0:
            for vicar in self.vicar.vicars:
                if ('(' in vicar):
                    vicarEntry = ElementTree.SubElement(entry, 'vicar')
                    ElementTree.SubElement(vicarEntry, 'name').text = vicar[:vicar.find('(')].strip()
                    vicarData = self.analyzeDate(vicar)
                    if (len(vicarData[0]) > 3):
                        ElementTree.SubElement(vicarEntry, 'date').text = vicarData[0].strip()
                    if (len(vicarData[2]) > 2):
                        ElementTree.SubElement(vicarEntry, 'misc').text = vicarData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'vicar').text = vicar.strip()
        del(self.vicar.vicars[:])

        #Pastors
        if len(self.vicar.pastors) > 0:
            for pastor in self.vicar.pastors:
                if ('(' in pastor):
                    pastorEntry = ElementTree.SubElement(entry, 'pastor')
                    ElementTree.SubElement(pastorEntry, 'name').text = pastor[:pastor.find('(')].strip()
                    pastorData = self.analyzeDate(pastor)
                    if (len(pastorData[0]) > 3):
                        ElementTree.SubElement(pastorEntry, 'date').text = pastorData[0].strip()
                    if (len(pastorData[2]) > 2):
                        ElementTree.SubElement(pastorEntry, 'misc').text = pastorData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'pastor').text = pastor.strip()
        del(self.vicar.pastors[:])

        #Institutions
        if len(self.vicar.institutions) > 0:
            for institution in self.vicar.institutions:
                if ('(' in institution):
                    institutionEntry = ElementTree.SubElement(entry, 'institution')
                    ElementTree.SubElement(institutionEntry, 'name').text = institution[:institution.find('(')].strip()
                    institutionData = self.analyzeDate(institution)
                    if (len(institutionData[0]) > 3):
                        ElementTree.SubElement(institutionEntry, 'date').text = institutionData[0].strip()
                    if (len(institutionData[2]) > 2):
                        ElementTree.SubElement(institutionEntry, 'misc').text = institutionData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'institution').text = institution.strip()
        del(self.vicar.institutions[:])

        #Teachers
        if len(self.vicar.teachers) > 0:
            for teacher in self.vicar.teachers:
                if ('(' in teacher):
                    teacherEntry = ElementTree.SubElement(entry, 'teacher')
                    ElementTree.SubElement(teacherEntry, 'name').text = teacher[:teacher.find('(')].strip()
                    teacherData = self.analyzeDate(teacher)
                    if (len(teacherData[0]) > 3):
                        ElementTree.SubElement(teacherEntry, 'date').text = teacherData[0].strip()
                    if (len(teacherData[2]) > 2):
                        ElementTree.SubElement(teacherEntry, 'misc').text = teacherData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'teacher').text = teacher.strip()
        del(self.vicar.teachers[:])

        #Education
        if len(self.vicar.education) > 0:
            for education in self.vicar.education:
                if ('(' in education):
                    educationEntry = ElementTree.SubElement(entry, 'education')
                    ElementTree.SubElement(educationEntry, 'name').text = education[:education.find('(')].strip()
                    educationData = self.analyzeDate(education)
                    if (len(educationData[0]) > 3):
                        ElementTree.SubElement(educationEntry, 'date').text = educationData[0].strip()
                    if (len(educationData[2]) > 2):
                        ElementTree.SubElement(educationEntry, 'misc').text = educationData[2].strip()
                else:
                    ElementTree.SubElement(entry, 'education').text = education.strip()
        del(self.vicar.education[:])

        #Misc
        if (self.vicar.misc is not None):
            ElementTree.SubElement(entry, 'misc').text = self.vicar.misc.strip()

        #Archive
        if (self.vicar.archive is not None):
            ElementTree.SubElement(entry, 'archive').text = self.vicar.archive.strip()

        #Literature
        if (self.vicar.literature is not None):
            ElementTree.SubElement(entry, 'literature').text = self.vicar.literature.strip()
        return entry

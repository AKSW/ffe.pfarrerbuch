# -*- coding: utf-8 -*-

"""
Class for analyzing a certain segment and creating a corresponding output

Author: Robert R.
"""

from vicar import Vicar
from analyzer import Analyzer
import re
import xml.etree.ElementTree as ElementTree


class SegmentAnalyzer:

    eventId = 0

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
        #0 = surname
        #1 = surname variations
        #2 = forename
        #3 = forename variations

        commaSplit = name.split(',');

        if (len(commaSplit) < 2):
            splitname[0] = name
        elif ('(' not in name):
            splitname[0] = commaSplit[0]
            splitname[2] = commaSplit[1]

        #one bracket
        elif (name.find('(') == name.rfind('(')):
            #surname bracket -> before comma
            if (name.find('(') < name.find(',')):
                splitname[0] = name[:name.find('(')]
                splitname[1] = name[name.find('(') + 1:name.find(')')]
                splitname[2] = name[name.find(')') + 2:]
            #forename bracket
            else:
                splitname[0] = name[:name.find(',')]
                splitname[2] = name[name.find(',') + 1:name.find('(')]
                splitname[3] = name[name.find('(') + 1:name.find(')')]

        #two brackets
        else:
            splitname[0] = name[:name.find('(')]
            splitname[1] = name[name.find('(') + 1:name.find(')')]
            splitname[2] = name[name.find(')') + 2:name.rfind('(')]
            splitname[3] = name[name.rfind('(') + 1:name.rfind(')')]

        return splitname

    def parsedate(self, text):
        date = ['0'] * 2
        if (re.search('\d+.\d+.\d+', text)):
            date[0] = re.findall('\d+.\d+.\d+', text)[0]
        elif (re.search('\d+.\d+', text)):
            date[0] = re.findall('\d+.\d+', text)[0]
        elif (re.search('\d\d\d\d', text)):
            date[0] = re.findall('\d\d\d\d', text)[0]
        if ('k.' in text):
            date[1] = 'k.'
        elif ('e.' in text):
            date[1] = 'e.'
        elif ('előtt' in text):
            date[1] = 'előtt'
        elif ('u.' in text):
            date[1] = 'u.'
        elif ('után' in text):
            date[1] = 'után'
        elif ('?' in text):
            date[1] = '?'
        return date

    def analyzeBrackets(self, text):
        analyzed = ['0'] * 3
        #0 = date inaccuracy (if any, otherwise 0)'
        #1 = date
        #2 = place

        #only one bracket
        if ('(' in text and text.find('(') == text.rfind('(')):
            bracket = text[text.find('(') + 1:text.find(')')]
            #bracket contains date
            if (re.search('\d+', bracket)):
                if (re.search('\d+-\d+', bracket)):
                    analyzed[1] = re.findall('\d+-\d+', bracket)[0]
                elif (re.search('\d+-', bracket)):
                    analyzed[1] = re.findall('\d+-', bracket)[0]
                elif (re.search('\d\d\d\d', bracket)):
                    analyzed[1] = re.findall('\d\d\d\d', bracket)[0]
                #date inaccuracy
                if ('k.' in bracket):
                    analyzed[0] = 'k.'
                elif ('e.' in bracket):
                    analyzed[0] = 'e.'
                elif ('előtt' in bracket):
                    analyzed[0] = 'előtt'
                elif ('u.' in bracket):
                    analyzed[0] = 'u.'
                elif ('után' in bracket):
                    analyzed[0] = 'után'
                elif ('?' in bracket):
                    analyzed[0] = '?'
            #bracket contains place
            else:
                analyzed[2] = bracket

        #two brackets
        else:
            bracket1 = text[text.find('(') + 1:text.find(')')]
            bracket2 = text[text.rfind('(') + 1:text.rfind(')')]
            #bracket1 handling
            if (re.search('\d+', bracket1)):
                if (re.search('\d+-\d+', bracket1)):
                    analyzed[1] = re.findall('\d+-\d+', bracket1)[0]
                elif (re.search('\d+-', bracket1)):
                    analyzed[1] = re.findall('\d+-', bracket1)[0]
                elif (re.search('\d\d\d\d', bracket1)):
                    analyzed[1] = re.findall('\d\d\d\d', bracket1)[0]
                if ('k.' in bracket1):
                    analyzed[0] = 'k.'
                elif ('e.' in bracket1):
                    analyzed[0] = 'e.'
                elif ('előtt' in bracket1):
                    analyzed[0] = 'előtt'
                elif ('u.' in bracket1):
                    analyzed[0] = 'u.'
                elif ('után' in bracket1):
                    analyzed[0] = 'után'
                elif ('?' in bracket1):
                    analyzed[0] = '?'
            else:
                analyzed[2] = bracket1
            #bracket2 handling
            if (re.search('\d+', bracket2)):
                if (re.search('\d+-\d+', bracket2)):
                    analyzed[1] = re.findall('\d+-\d+', bracket2)[0]
                elif (re.search('\d+-', bracket2)):
                    analyzed[1] = re.findall('\d+-', bracket2)[0]
                elif (re.search('\d\d\d\d', bracket2)):
                    analyzed[1] = re.findall('\d\d\d\d', bracket2)[0]
                if ('k.' in bracket2):
                    analyzed[0] = 'k.'
                elif ('e.' in bracket2):
                    analyzed[0] = 'e.'
                elif ('előtt' in bracket2):
                    analyzed[0] = 'előtt'
                elif ('u.' in bracket2):
                    analyzed[0] = 'u.'
                elif ('után' in bracket2):
                    analyzed[0] = 'után'
                elif ('?' in bracket2):
                    analyzed[0] = '?'
            else:
                analyzed[2] = bracket2
        return analyzed

    def createSubentries(self, vicarElement, elementName, entry, idToggle, bracket):
        if (idToggle):
            for element in vicarElement:
                elementEntry = ElementTree.SubElement(entry, elementName)
                elementEntry.set('id', str(self.vicar.id) + '-' + str(self.eventId))
                self.eventId += 1
                if ('(' in element):
                    elementData = self.analyzeBrackets(element)
                    if (len(elementData[2]) > 2 and bracket):
                        ElementTree.SubElement(elementEntry, 'name').text = element[:element.find('(')].strip() + ' (' + elementData[2] + ')'
                    else:
                        ElementTree.SubElement(elementEntry, 'name').text = element[:element.find('(')].strip()
                    if (elementData[0] is not '0'):
                        if (len(elementData[1]) > 3):
                            ElementTree.SubElement(elementEntry, 'date').text = elementData[1].strip()
                            elementEntry.set('inaccuracy', str(elementData[0].strip()))
                    else:
                        if (len(elementData[1]) > 3):
                            ElementTree.SubElement(elementEntry, 'date').text = elementData[1].strip()
                    if (len(elementData[2]) > 2 and not bracket):
                        ElementTree.SubElement(elementEntry, 'place').text = elementData[2].strip()
                else:
                    ElementTree.SubElement(elementEntry, 'name').text = element.strip()
        else:
            for element in vicarElement:
                elementEntry = ElementTree.SubElement(entry, elementName)
                if ('(' in element):
                    elementData = self.analyzeBrackets(element)
                    if (len(elementData[2]) > 2 and bracket):
                        ElementTree.SubElement(elementEntry, 'name').text = element[:element.find('(')].strip() + ' (' + elementData[2] + ')'
                    else:
                        ElementTree.SubElement(elementEntry, 'name').text = element[:element.find('(')].strip()
                    if (elementData[0] is not '0'):
                        if (len(elementData[1]) > 3):
                            ElementTree.SubElement(elementEntry, 'date').text = elementData[1].strip()
                            elementEntry.set('inaccuracy', str(elementData[0].strip()))
                    else:
                        if (len(elementData[1]) > 3):
                            ElementTree.SubElement(elementEntry, 'date').text = elementData[1].strip()
                    if (len(elementData[2]) > 2):
                        ElementTree.SubElement(elementEntry, 'place').text = elementData[2].strip()
                else:
                    ElementTree.SubElement(elementEntry, 'name').text = element.strip()

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
                date = self.parsedate(self.vicar.ordination.strip())
                if (date[1] is not '0' and date[0] is not '0'):
                    ElementTree.SubElement(ordination, 'date').text = date[0].strip()
                    ordination.set('inaccuracy', str(date[1].strip()))
                elif (date[0] is not '0'):
                    ElementTree.SubElement(ordination, 'date').text = date[0]

        #birthday
        if (self.vicar.birthday is not None):
            birthday = ElementTree.SubElement(entry, 'birthday')
            ElementTree.SubElement(birthday, 'place').text = self.vicar.birthday.strip().split(',')[0]
            if (len(self.vicar.birthday.strip().split(',')) == 2):
                date = self.parsedate(self.vicar.birthday.strip())
                if (date[1] is not '0' and date[0] is not '0'):
                    ElementTree.SubElement(birthday, 'date').text = date[0].strip()
                    birthday.set('inaccuracy', str(date[1].strip()))
                elif (date[0] is not '0'):
                    ElementTree.SubElement(birthday, 'date').text = date[0]

        #obit
        if (self.vicar.obit is not None):
            obit = ElementTree.SubElement(entry, 'obit')
            ElementTree.SubElement(obit, 'place').text = self.vicar.obit.strip().split(',')[0]
            if (len(self.vicar.obit.strip().split(',')) == 2):
                date = self.parsedate(self.vicar.obit.strip())
                if (date[1] is not '0' and date[0] is not '0'):
                    ElementTree.SubElement(obit, 'date').text = date[0].strip()
                    obit.set('inaccuracy', str(date[1].strip()))
                elif (date[0] is not '0'):
                    ElementTree.SubElement(obit, 'date').text = date[0]

        #Father
        if (self.vicar.father is not None):
            ElementTree.SubElement(entry, 'father').text = self.vicar.father.strip()

        #Mother
        if (self.vicar.mother is not None):
            ElementTree.SubElement(entry, 'mother').text = self.vicar.mother.strip()

        #Siblings
        if len(self.vicar.siblings) > 0:
            self.createSubentries(self.vicar.siblings, 'sibling', entry, False, True)
        del(self.vicar.siblings[:])

        #Offspring
        if len(self.vicar.offspring) > 0:
            self.createSubentries(self.vicar.offspring, 'offspring', entry, False, True)
        del(self.vicar.offspring[:])

        #Vicars
        if len(self.vicar.vicars) > 0:
            self.createSubentries(self.vicar.vicars, 'vicar', entry, False, True)
        del(self.vicar.vicars[:])

        #Pastors
        if len(self.vicar.pastors) > 0:
            self.createSubentries(self.vicar.pastors, 'pastor', entry, True, True)
        del(self.vicar.pastors[:])

        #Institutions
        if len(self.vicar.institutions) > 0:
            self.createSubentries(self.vicar.institutions, 'institution', entry, True, True)
        del(self.vicar.institutions[:])

        #Teachers
        if len(self.vicar.teachers) > 0:
            self.createSubentries(self.vicar.teachers, 'teacher', entry, True, True)
        del(self.vicar.teachers[:])

        #Education
        if len(self.vicar.education) > 0:
            self.createSubentries(self.vicar.education, 'education', entry, True, True)
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

        #original
        if (self.vicar.original is not None):
            text = '\n'
            for line in self.vicar.original:
                text = text + line
            ElementTree.SubElement(entry, 'original').text = text
        return entry

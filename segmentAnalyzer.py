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
        #0 = surname
        #1 = surname variations
        #2 = forename
        #3 = forename variations

        if ('(' not in name):
            splitname[0] = name.split(',')[0]
            splitname[2] = name.split(',')[1]

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
        #if (re.search('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', text)):
            #date[1] = re.findall('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', text)[0]
        #print (date)
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
                #if (re.search('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', bracket)):
                    #analyzed[0] = re.findall('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', bracket)[0]
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
                #if (re.search('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', bracket1)):
                    #analyzed[0] = re.findall('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', bracket1)[0]
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
                #if (re.search('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', bracket2)):
                    #analyzed[0] = re.findall('\bk.\b|\be.\b|\belőtt\b|\bu.\b|\bután\b|[?]', bracket2)[0]
            else:
                analyzed[2] = bracket2
        #print (analyzed)
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
            for sibling in self.vicar.siblings:
                siblingEntry = ElementTree.SubElement(entry, 'sibling')
                if ('(' in sibling):
                    ElementTree.SubElement(siblingEntry, 'name').text = sibling[:sibling.find('(')].strip()
                    siblingData = self.analyzeBrackets(sibling)
                    if (siblingData[0] is not '0'):
                        if (len(siblingData[1]) > 3):
                            ElementTree.SubElement(siblingEntry, 'date').text = siblingData[1].strip()
                            siblingEntry.set('inaccuracy', str(siblingData[0].strip()))
                    else:
                        if (len(siblingData[1]) > 3):
                            ElementTree.SubElement(siblingEntry, 'date').text = siblingData[1].strip()
                    if (len(siblingData[2]) > 2):
                        ElementTree.SubElement(siblingEntry, 'place').text = siblingData[2].strip()
                else:
                    ElementTree.SubElement(siblingEntry, 'name').text = sibling.strip()
        del(self.vicar.siblings[:])

        #Offspring
        if len(self.vicar.offspring) > 0:
            for offspring in self.vicar.offspring:
                offspringEntry = ElementTree.SubElement(entry, 'offspring')
                if ('(' in offspring):
                    ElementTree.SubElement(offspringEntry, 'name').text = offspring[:offspring.find('(')].strip()
                    offspringData = self.analyzeBrackets(offspring)
                    if (offspringData[0] is not '0'):
                        if (len(offspringData[1]) > 3):
                            ElementTree.SubElement(offspringEntry, 'date').text = offspringData[1].strip()
                            offspringEntry.set('inaccuracy', str(offspringData[0].strip()))
                    else:
                        if (len(offspringData[1]) > 3):
                            ElementTree.SubElement(offspringEntry, 'date').text = offspringData[1].strip()
                    if (len(offspringData[2]) > 2):
                        ElementTree.SubElement(offspringEntry, 'place').text = offspringData[2].strip()
                else:
                    ElementTree.SubElement(offspringEntry, 'name').text = offspring.strip()
        del(self.vicar.offspring[:])

        #Vicars
        if len(self.vicar.vicars) > 0:
            for vicar in self.vicar.vicars:
                vicarEntry = ElementTree.SubElement(entry, 'vicar')
                if ('(' in vicar):
                    ElementTree.SubElement(vicarEntry, 'name').text = vicar[:vicar.find('(')].strip()
                    vicarData = self.analyzeBrackets(vicar)
                    if (vicarData[0] is not '0'):
                        if (len(vicarData[1]) > 3):
                            ElementTree.SubElement(vicarEntry, 'date').text = vicarData[1].strip()
                            vicarEntry.set('inaccuracy', str(vicarData[0].strip()))
                    else:
                        if (len(vicarData[1]) > 3):
                            ElementTree.SubElement(vicarEntry, 'date').text = vicarData[1].strip()
                    if (len(vicarData[2]) > 2):
                        ElementTree.SubElement(vicarEntry, 'place').text = vicarData[2].strip()
                else:
                    ElementTree.SubElement(vicarEntry, 'name').text = vicar.strip()
        del(self.vicar.vicars[:])

        eventId = 0
        #Pastors
        if len(self.vicar.pastors) > 0:
            for pastor in self.vicar.pastors:
                pastorEntry = ElementTree.SubElement(entry, 'pastor')
                pastorEntry.set('id', str(self.vicar.id) + '-' + str(eventId))
                eventId += 1
                if ('(' in pastor):
                    ElementTree.SubElement(pastorEntry, 'name').text = pastor[:pastor.find('(')].strip()
                    pastorData = self.analyzeBrackets(pastor)
                    if (pastorData[0] is not '0'):
                        if (len(pastorData[1]) > 3):
                            ElementTree.SubElement(pastorEntry, 'date').text = pastorData[1].strip()
                            pastorEntry.set('inaccuracy', str(pastorData[0].strip()))
                    else:
                        if (len(pastorData[1]) > 3):
                            ElementTree.SubElement(pastorEntry, 'date').text = pastorData[1].strip()
                    if (len(pastorData[2]) > 2):
                        ElementTree.SubElement(pastorEntry, 'place').text = pastorData[2].strip()
                else:
                    ElementTree.SubElement(pastorEntry, 'name').text = pastor.strip()
        del(self.vicar.pastors[:])

        #Institutions
        if len(self.vicar.institutions) > 0:
            for institution in self.vicar.institutions:
                institutionEntry = ElementTree.SubElement(entry, 'institution')
                institutionEntry.set('id', str(self.vicar.id) + '-' + str(eventId))
                eventId += 1
                if ('(' in institution):
                    ElementTree.SubElement(institutionEntry, 'name').text = institution[:institution.find('(')].strip()
                    institutionData = self.analyzeBrackets(institution)
                    if (institutionData[0] is not '0'):
                        if (len(institutionData[1]) > 3):
                            ElementTree.SubElement(institutionEntry, 'date').text = institutionData[1].strip()
                            institutionEntry.set('inaccuracy', str(institutionData[0].strip()))
                    else:
                        if (len(institutionData[1]) > 3):
                            ElementTree.SubElement(institutionEntry, 'date').text = institutionData[1].strip()
                    if (len(institutionData[2]) > 2):
                        ElementTree.SubElement(institutionEntry, 'place').text = institutionData[2].strip()
                else:
                    ElementTree.SubElement(institutionEntry, 'name').text = institution.strip()
        del(self.vicar.institutions[:])

        #Teachers
        if len(self.vicar.teachers) > 0:
            for teacher in self.vicar.teachers:
                teacherEntry = ElementTree.SubElement(entry, 'teacher')
                teacherEntry.set('id', str(self.vicar.id) + '-' + str(eventId))
                eventId += 1
                if ('(' in teacher):
                    ElementTree.SubElement(teacherEntry, 'name').text = teacher[:teacher.find('(')].strip()
                    teacherData = self.analyzeBrackets(teacher)
                    if (teacherData[0] is not '0'):
                        if (len(teacherData[1]) > 3):
                            ElementTree.SubElement(teacherEntry, 'date').text = teacherData[1].strip()
                            teacherEntry.set('inaccuracy', str(teacherData[0].strip()))
                    else:
                        if (len(teacherData[1]) > 3):
                            ElementTree.SubElement(teacherEntry, 'date').text = teacherData[1].strip()
                    if (len(teacherData[2]) > 2):
                        ElementTree.SubElement(teacherEntry, 'place').text = teacherData[2].strip()
                else:
                    ElementTree.SubElement(teacherEntry, 'name').text = teacher.strip()
        del(self.vicar.teachers[:])

        #Education
        if len(self.vicar.education) > 0:
            for education in self.vicar.education:
                educationEntry = ElementTree.SubElement(entry, 'education')
                educationEntry.set('id', str(self.vicar.id) + '-' + str(eventId))
                eventId += 1
                if ('(' in education):
                    ElementTree.SubElement(educationEntry, 'name').text = education[:education.find('(')].strip()
                    educationData = self.analyzeBrackets(education)
                    if (educationData[0] is not '0'):
                        if (len(educationData[1]) > 3):
                            ElementTree.SubElement(educationEntry, 'date').text = educationData[1].strip()
                            educationEntry.set('inaccuracy', str(educationData[0].strip()))
                    else:
                        if (len(educationData[1]) > 3):
                            ElementTree.SubElement(educationEntry, 'date').text = educationData[1].strip()
                    if (len(educationData[2]) > 2):
                        ElementTree.SubElement(educationEntry, 'place').text = educationData[2].strip()
                else:
                    ElementTree.SubElement(educationEntry, 'name').text = education.strip()
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

# -*- coding: utf-8 -*-

"""
Class for analyzing a certain input string

Author: Robert R.
"""

from vicar import Vicar


class Analyzer:

    def __init__(self, inputLine, vicar):            # initilization
        self.inputLine = inputLine
        self.vicar = vicar

    def parseOrdination(self):
        if 'Ord.:' == self.inputLine[:5] and len(self.inputLine) > 8:
            self.vicar.ordination = self.inputLine[6:]

    def parseBirthday(self):
        if '*' == self.inputLine[0] and len(self.inputLine) > 6:
            self.vicar.birthday = self.inputLine[2:]

    def parseObit(self):
        if '†' == self.inputLine[0] and len(self.inputLine) > 6:
            self.vicar.obit = self.inputLine[2:]

    def parseMarried(self):
        if '8' == self.inputLine[0] and len(self.inputLine) > 6:
            self.vicar.inputLine = self.inputLine[2:]

    def parseFather(self):                    # parse father
        if 'P:' == self.inputLine[:2] and len(self.inputLine) > 6:
            self.vicar.father = self.inputLine[3:]

    def parseMother(self):
        if 'M:' == self.inputLine[:2] and len(self.inputLine) > 6:
            self.vicar.mother = self.inputLine[3:]

    def parseSiblings(self):
        if 'Fr:' == self.inputLine[:3] and len(self.inputLine) > 7:
            self.vicar.siblings[:] = self.inputLine[4:].split(',')
            for i, sibling in enumerate(self.vicar.siblings):
                if ")" in sibling and not "(" in sibling:
                    self.vicar.siblings[i-1] = self.vicar.siblings[i-1] + ', ' + sibling
                    self.vicar.siblings.remove(sibling)

    def parseOffspring(self):
        if 'Fi:' == self.inputLine[:3] and len(self.inputLine) > 7:
            self.vicar.offspring[:] = self.inputLine[4:].split(',')
            for i, offspring in enumerate(self.vicar.offspring):
                if ")" in offspring and not "(" in offspring:
                    self.vicar.offspring[i-1] = self.vicar.offspring[i-1] + ', ' + offspring
                    self.vicar.offspring.remove(offspring)

    def parseVicars(self):
        if 'V:' == self.inputLine[:2] and len(self.inputLine) > 6:
            self.vicar.vicars[:] = self.inputLine[3:].split(',')
            for i, vicar in enumerate(self.vicar.vicars):
                if ")" in vicar and not "(" in vicar:
                    self.vicar.vicars[i-1] = self.vicar.vicars[i-1] + ', ' + vicar
                    self.vicar.vicars.remove(vicar)

    def parsePastors(self):
        if 'VDM:' == self.inputLine[:4] and len(self.inputLine) > 8:
            self.vicar.pastors[:] = self.inputLine[5:].split(',')
            for i, pastor in enumerate(self.vicar.pastors):
                if ")" in pastor and not "(" in pastor:
                    self.vicar.pastors[i-1] = self.vicar.pastors[i-1] + ', ' + pastor
                    self.vicar.pastors.remove(pastor)

    def parseInstitutions(self):
        if 'S:' == self.inputLine[:2] and len(self.inputLine) > 6:
            self.vicar.institutions[:] = self.inputLine[3:].split(',')
            for i, institution in enumerate(self.vicar.institutions):
                if ")" in institution and not "(" in institution:
                    self.vicar.institutions[i-1] = self.vicar.institutions[i-1] + ', ' + institution
                    self.vicar.institutions.remove(institution)

    def parseTeachers(self):
        if 'LM:' == self.inputLine[:3] and len(self.inputLine) > 7:
            self.vicar.teachers[:] = self.inputLine[4:].split(',')
            for i, teacher in enumerate(self.vicar.teachers):
                if ")" in teacher and not "(" in teacher:
                    self.vicar.teachers[i-1] = self.vicar.teachers[i-1] + ', ' + teacher
                    self.vicar.teachers.remove(teacher)

    def parseEducation(self):
        if 'St:' == self.inputLine[:3] and len(self.inputLine) > 7:
            self.vicar.education[:] = self.inputLine[4:].split(',')
            for i, education in enumerate(self.vicar.education):
                if ")" in education and not "(" in education:
                    self.vicar.education[i-1] = self.vicar.education[i-1] + ', ' + education
                    self.vicar.education.remove(education)

    def parseMisc(self):
        if 'N:' == self.inputLine[:2] and len(self.inputLine) > 6:
            self.vicar.misc = self.inputLine[3:]

    def parseArchive(self):
        if 'A:' == self.inputLine[:2] and len(self.inputLine) > 6:
            self.vicar.archive = self.inputLine[3:]

    def parseLiterature(self):
        if 'Lit:' == self.inputLine[:4] and len(self.inputLine) > 8:
            self.vicar.literature = self.inputLine[5:]

    def analyze(self):                        # general analyzation of input
        self.parseArchive()
        self.parseBirthday()
        self.parseEducation()
        self.parseFather()
        self.parseInstitutions()
        self.parseLiterature()
        self.parseMarried()
        self.parseMisc()
        self.parseMother()
        self.parseObit()
        self.parseOffspring()
        self.parseOrdination()
        self.parsePastors()
        self.parseSiblings()
        self.parseTeachers()
        self.parseVicars()

def main():                                        # main class (testing)
    text = 'T. Konrad, * Bucha b. Jena 21.08.1872 '
    analyzer = Analyzer(text)
    output = analyzer.analyze()
    print(analyzer.analyze())
    vicar = Vicar()
    print(vicar.birthday)
    print(vicar.obit)

if __name__ == '__main__':                # call if module is called as main
    main()

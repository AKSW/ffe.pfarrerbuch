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
        if 'Ord.:' == self.inputLine[0:4] and len(self.inputLine) > 8:
            self.vicar.ordination = self.inputLine[6:]

    def parseBirthday(self):
        if '*' == self.inputLine[0] and len(self.inputLine) > 6:
            self.vicar.birthday = self.inputLine[2:]

    def parseObit(self):
        if '†' == self.inputLine[0] and len(self.inputLine) > 6:
            self.vicar.obibit = self.inputLine[2:]

    def parseMarried(self):
        if '8' == self.inputLine[0] and len(self.inputLine) > 6:
            self.vicar.inputLine = self.inputLine[2:]

    def parseFather(self):                    # parse father
        if 'P:' == self.inputLine[:1] and len(self.inputLine) > 6:
            self.vicar.father = self.inputLine[3:]

    def parseMother(self):
        if 'M:' == self.inputLine[:1] and len(self.inputLine) > 6:
            self.vicar.mother = self.inputLine[3:]

    def parseSiblings(self):
        if 'Fr:' == self.inputLine[:2] and len(self.inputLine) > 7:
            self.vicar.siblings[:] = self.inputLine[4:].split(',')

    def parseOffspring(self):
        if 'Fi:' == self.inputLine[:2] and len(self.inputLine) > 7:
            self.vicar.offspring[:] = self.inputLine[4:].split(',')

    def parseVicars(self):
        if 'V:' == self.inputLine[:1] and len(self.inputLine) > 6:
            self.vicar.vicars[:] = self.inputLine[3:].split(',')

    def parsePastors(self):
        if 'VDM:' == self.inputLine[:4] and len(self.inputLine) > 8:
            self.vicar.pastors[:] = self.inputLine[5:].split(',')

    def parseInstitutions(self):
        if 'S:' == self.inputLine[:1] and len(self.inputLine) > 6:
            self.vicar.institutions[:] = self.inputLine[3:].split(',')

    def parseTeachers(self):
        if 'LM:' == self.inputLine[:2] and len(self.inputLine) > 7:
            self.vicar.teachers[:] = self.inputLine[4:].split(',')

    def parseEducation(self):
        if 'St:' == self.inputLine[:2] and len(self.inputLine) > 7:
            self.vicar.education[:] = self.inputLine[4:]

    def parseMisc(self):
        if 'N:' == self.inputLine[:1] and len(self.inputLine) > 6:
            self.vicar.misc[:] = self.inputLine[3:]

    def parseArchive(self):
        if 'A:' == self.inputLine[:1] and len(self.inputLine) > 6:
            self.vicar.archive[:] = self.inputLine[3:]

    def parseLiterature(self):
        if 'Lit:' == self.inputLine[:4] and len(self.inputLine) > 8:
            self.vicar.pastors[:] = self.inputLine[5:]

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
    vicar = Vicar('k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.'
                  'k.A.', 'k.A.', 'k.A.')
    print(vicar.birthday)
    print(vicar.obit)

if __name__ == '__main__':                # call if module is called as main
    main()

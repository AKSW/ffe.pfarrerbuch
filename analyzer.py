# -*- coding: utf-8 -*-

"""
Class for analyzing a certain input string

Author: Robert R.
"""

from vicar import Vicar


class Analyzer:

    def __init__(self, inputLine):            # initilization
        self.inputLine = inputLine

    def parseBirthdayObit(self):              # parsing birth and obit
        if ',' in self.inputLine:
            birthday = self.inputLine[2:self.inputLine.index(',')]
            obit = self.inputLine[(self.inputLine.index(',') + 6):]
            if len(birthday) < 3:
                birthday = 'k.A.'
            if len(obit) < 2:
                obit = 'k.A.'
        else:
            birthday = 'k.A.'
            obit = 'k.A.'
        return ['dates', birthday, obit]

    def parseFather(self):                    # parse father
        if ';' in self.inputLine:
            return self.inputLine[3:self.inputLine.index(';')]
        else:
            return self.inputLine[3:]

    def parseMother(self):                    # parse mother
        if ';' in self.inputLine:
            return self.inputLine[self.inputLine.index(';') + 5:]
        else:
            return 'k.A.'

    def parseOrdination(self):                # parse ordination
        if len(self.inputLine[5:]) < 3:
            return ['ordination', 'k.A.']
        else:
            return ['ordination', self.inputLine[5:]]

    def parseSon(self):                       # parse son
        return ['son', self.inputLine[3:]]

    def parseDaughter(self):                  # parse daughter
        return ['daughter', self.inputLine[3:]]

    def parseOther(self):                     # parse misc
        return ['misc', self.inputLine]

    def analyze(self):                        # general analyzation of input
        if self.inputLine[0] == '*':
            output = self.parseBirthdayObit()
        elif 'V:' and 'M:' in self.inputLine and 'V:' == self.inputLine[0:2]:
            output = ['parents', self.parseFather(), self.parseMother()]
        elif 'V:' in self.inputLine and 'V:' == self.inputLine[0:2]:
            output = ['father', self.parseFather()]
        elif 'M:' in self.inputLine:
            output = ['mother', self.parseMother()]
        elif 'ord.' in self.inputLine:
            output = self.parseOrdination()
        elif self.inputLine[0:2] == 'T.':
            output = self.parseDaughter()
        elif self.inputLine[0:2] == 'S.':
            output = self.parseSon()
        else:
            output = self.parseOther()
        return output


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

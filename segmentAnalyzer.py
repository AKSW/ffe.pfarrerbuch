
from vicar import Vicar
from analyzer import Analyzer

import re

class SegmentAnalyzer:

    def __init__(self, segment, vicar):
        self.segment = segment
        self.vicar = vicar

    def analyze(self):
        for i, line in enumerate(self.segment):
            if line != '\n' and i < 2 and line[0] != '*':
                self.vicar.name = line
                continue
            elif line != '\n':
                analyzer = Analyzer(line)
                output = analyzer.analyze()
            else:
                continue
            if output[0] == 'dates':
                self.vicar.birthday = output[1]
                self.vicar.obit = output[2]
            elif output[0] == 'parents':
                self.vicar.father = output[1]
                self.vicar.mother = output[2]
            elif output[0] == 'father':
                self.vicar.father = output[1]
            elif output[0] == 'mother':
                self.vicar.mother = output[1]
            elif output[0] == 'ordination':
                self.vicar.ordination = output[1]
            elif output[0] == 'son' or 'daughter':
                if self.vicar.offspring == 'k.A.':
                    self.vicar.offspring = output
                elif (self.segment[i - 1])[0:2] == 'S.' or 'T.':
                    (self.vicar.offspring[-1:])[1] = (self.vicar.offspring[-1:])[1] + line
                    n = i + 1
                    while (self.segment[n])[0:2] != 'S.' or 'T.':
                        (self.vicar.offspring[-1:])[1] = (self.vicar.offspring[-1:])[1] + self.segment[n]
                        self.segment[n] = '\n'
                        n = n + 1
            elif output[0] == 'misc':
                self.vicar.misc = self.vicar.misc + output[1]
        return self.vicar

    def createEntry(self):
        self.analyze()
        output = ('\t<vicar>\n\t\t<name>\n\t\t\t' + self.vicar.name +
        '\n\t\t</name>\n\t\t<birthday>\n\t\t\t' + self.vicar.birthday +
        '\n\t\t</birthday>\n\t\t<obit>\n\t\t\t' + self.vicar.obit +
        '\n\t\t</obit>\n\t\t<father>\n\t\t\t' + self.vicar.father +
        '\n\t\t</father>\n\t\t<mother>\n\t\t\t' + self.vicar.mother +
        '\n\t\t</mother>\n\t\t<ordination>\n\t\t\t' + self.vicar.ordination +
        '\n\t\t</ordination>\n\t\t<offspring>\n\t\t\t')
        if self.vicar.offspring[0] == 'k.A.':
            for children in self.vicar.offspring:
                if children[0] == 'son':
                    output = (output + '<son>\n\t\t\t\t' + children[1] +
                    '\n\t\t\t</son>\n\t\t\t')
                elif children[0] == 'daughter':
                    output = (output + '<daughter>\n\t\t\t\t' + children[1] +
                    '\n\t\t\t</daughter>\n\t\t\t')
            output = output = '\n\t\t'
        else:
            output = output + 'k.A.\n\t\t'
        output = (output + '</offspring>\n\t\t<misc>\n\t\t\t' +
        self.vicar.misc + '\n\t\t</misc>\n\t</vicar>\n\n')
        return output

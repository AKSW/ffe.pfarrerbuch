
from vicar import Vicar
from analyzer import Analyzer

import re

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

    def createEntry(self):
        self.analyze()
        output = (
            '\t<vicar>\n' +
            '\t\t<name>\n' +
            '\t\t\t'+ self.vicar.name +
            '\t\t</name>' +
            '\t\t<ordination>\n' +
            '\t\t\t'+ self.vicar.ordination +
            '\t\t</ordination>\n' +
            '\t\t<birthday>\n' +
            '\t\t\t'+ self.vicar.birthday +
            '\t\t</birthday>\n'+
            '\t\t<obit>\n'
            '\t\t\t'+ self.vicar.obit +
            '\t\t</obit>\n'+
            '\t\t<married>\n'+
            '\t\t\t'+ self.vicar.married +
            '\t\t</married>\n'+
            '\t\t<father>\n'+
            '\t\t\t'+ self.vicar.father +
            '\t\t</father>\n'+
            '\t\t<mother>\n'+
            '\t\t\t'+ self.vicar.mother +
            '\t\t</mother>\n')
        if len(self.vicar.siblings) > 1:
            for sibling in self.vicar.siblings:
                output = output +
                '\t\t<sibling>\n' +
                '\t\t\t'+ sibling + '\n' +
                '\t\t</sibling>\n'
        else:
            output = output +
            '\t\t<sibling>\n' +
            '\t\t\t'+ self.vicar.siblings[0] + '\n' +
            '\t\t</sibling>\n'
        if len(self.vicar.offspring) > 1:
            for offspring in self.vicar.offspring:
                output = output +
                '\t\t<offspring>\n' +
                '\t\t\t'+ offspring + '\n' +
                '\t\t</offspring>\n'
        else:
            output = output +
            '\t\t<offspring>\n' +
            '\t\t\t'+ self.vicar.offspring[0] + '\n' +
            '\t\t</offspring>\n'
        if len(self.vicar.vicars) > 1:
            for vicar in self.vicar.vicars:
                output = output +
                '\t\t<vicar>\n' +
                '\t\t\t'+ vicar + '\n' +
                '\t\t</vicar>\n'
        else:
            output = output +
            '\t\t<vicar>\n' +
            '\t\t\t'+ self.vicar.vicars[0] + '\n' +
            '\t\t</vicar>\n'
        if len(self.vicar.pastors) > 1:
            for pastor in self.vicar.pastors:
                output = output +
                '\t\t<pastor>\n' +
                '\t\t\t'+ pastor + '\n' +
                '\t\t</pastor>\n'
        else:
            output = output +
            '\t\t<pastor>\n' +
            '\t\t\t'+ self.vicar.pastors[0] + '\n' +
            '\t\t</pastor>\n'
        if len(self.vicar.institutions) > 1:
            for institution in self.vicar.institutions:
                output = output +
                '\t\t<institution>\n' +
                '\t\t\t'+ institution + '\n' +
                '\t\t</institution>\n'
        else:
            output = output +
            '\t\t<institution>\n' +
            '\t\t\t'+ self.vicar.institutions[0] + '\n' +
            '\t\t</institution>\n'
        if len(self.vicar.teachers) > 1:
            for teacher in self.vicar.teachers:
                output = output +
                '\t\t<teacher>\n' +
                '\t\t\t'+ teacher + '\n' +
                '\t\t</teacher>\n'
        else:
            output = output +
            '\t\t<teacher>\n' +
            '\t\t\t'+ self.vicar.teachers[0] + '\n' +
            '\t\t</teacher>\n'
        output = output +
        '\t\t<education>\n'+
        '\t\t\t'+ self.vicar.education +
        '\t\t</education>\n'+
        '\t\t<misc>\n'+
        '\t\t\t'+ self.vicar.misc +
        '\t\t</misc>\n'+
        '\t\t<archive>\n'+
        '\t\t\t'+ self.vicar.archive +
        '\t\t</archive>\n'+
        '\t\t<literature>\n'+
        '\t\t\t'+ self.vicar.literature +
        '\t\t</literature>\n')
        return output

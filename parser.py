# -*- coding: utf-8 -*-

"""
Parser module which is relevant to parse a rawtext-file into a specific
XML - Format
Author: Robert R.
Version: 0.4

This file is the main-file and should be called as main in order to parse
a certain document

The project can be altered to fit for different needs

format convention of the raw-text:
    - name should be always in the first line of a new entry
    - no headers
    - no frontpages or other text besides the entries
    - birth needs to be indicated with *
    - father needs to be listed first with V:
    - mother needs to be listed with M:
    - daughter needs to be listed with T. and a son with S.
    - ordination needs to be adressed with ord.
    - the core information of each entry should never contain a blank line
    - a whole entry needs to have one blank line before the source

current bugs:
    - encoding in output file
    - misc is not properly parsed
    - education is not implemented
    - offspring does not work properly
"""

from analyzer import Analyzer
from vicar import Vicar
import codecs


class Parser:

    def __init__(self, fileName):
        self.filename = fileName

    def createVicarEntry(self, segment):
        """
        creates a new Vicar object
        initilizing vicar with 'k.A.' statements for "keine Angabe"
        """
        vicar = Vicar('k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.', 'k.A.',
                      'k.A.', 'k.A.')
        for i, line in enumerate(segment):
            if line != '\n' and i < 1:
                vicar.name = line
                continue
            elif line != '\n':
                analyzer = Analyzer(line)
                output = analyzer.analyze()
            else:
                continue
            if output[0] == 'dates':
                vicar.birthday = output[1]
                vicar.obit = output[2]
            elif output[0] == 'parents':
                vicar.father = output[1]
                vicar.mother = output[2]
            elif output[0] == 'father':
                vicar.father = output[1]
            elif output[0] == 'mother':
                vicar.mother = output[1]
            elif output[0] == 'ordination':
                vicar.ordination = output[1]
            elif output[0] == 'son' or 'daughter':
                if vicar.offspring[0] == 'k.A.':
                    vicar.offspring[0] = output
                elif (segment[i - 1])[0:2] == 'S.' or 'T.':
                    (vicar.offspring[-1])[1] = (vicar.offspring[-1])[1] + line
                    n = i + 1
                    while (segment[n])[0:2] != 'S.' or 'T.':
                        (vicar.offspring[-1])[1] = (vicar.offspring[-1])[1]
                        + segment[n]
                        del segment[n]
                        n = n + 1
            elif output[0] == 'misc':
                vicar.misc = vicar.misc + output[1]
        return vicar

    def readInputFile(self):              # reads the input file
        f = open(self.filename, 'r')
        text = []
        for line in f:
            text.append(line)
        f.close()
        return text

    def segmentation(self, text):         # creates segments from the text
        segments = []
        segment = []
        count = 0
        for line in text:
            if count == 1 and line == "\n":
                segment.append(line)
                count = 5
            elif count == 5 and line == "\n":
                segment.append(line)
                count = 0
                segments.append(segment[:])
                segment[:] = []
            elif count == 5 and line != "\n":
                segments.append(segment[:])
                segment[:] = []
                segment.append(line)
                count = 0
            elif count == 0 and line == "\n":
                segment.append(line)
                count = count + 1
            else:
                segment.append(line)
        return segments


def main():
    """
    main method for this project which creates the outputfile
    """
    parser = Parser('inputText.txt')
    output = open('outputText.txt', 'w+')
    output.write('<file>\n')
    for segment in parser.segmentation(parser.readInputFile()):
        vicar = parser.createVicarEntry(segment)
        output.write('\t<vicar>\n\t\t<name>\n\t\t\t' + vicar.name +
        '\n\t\t</name>\n\t\t<birthday>\n\t\t\t' + vicar.birthday +
        '\n\t\t</birthday>\n\t\t<obit>\n\t\t\t' + vicar.obit +
        '\n\t\t</obit>\n\t\t<father>\n\t\t\t' + vicar.father +
        '\n\t\t</father>\n\t\t<mother>\n\t\t\t' + vicar.mother +
        '\n\t\t</mother>\n\t\t<ordination>\n\t\t\t' + vicar.ordination +
        '\n\t\t</ordination>\n\t\t<offspring>\n\t\t\t')
        if vicar.offspring[0] == 'k.A.':
            for children in vicar.offspring:
                if children[0] == 'son':
                    output.write('<son>\n\t\t\t\t' + children[1] +
                    '\n\t\t\t</son>\n\t\t\t')
                elif children[0] == 'daughter':
                    output.write('<daughter>\n\t\t\t\t' + children[1] +
                    '\n\t\t\t</daughter>\n\t\t\t')
            output.write('\n\t\t')
        else:
            output.write('k.A.\n\t\t')
        output.write('</offspring>\n\t\t<misc>\n\t\t\t' + vicar.misc +
        '\n\t\t</misc>\n\t</vicar>\n\n')
    output.write('</file>')
    output.close()


"""    Test method to just segmentize all vicars
    parser = Parser('inputText.txt')
    output = open('outputText.txt', 'w+')
    output.write('<entry>\n')
    for segment in parser.segmentation(parser.readInputFile()):
        output.write('\t<segment>\n')
        for line in segment:
            output.write('\t\t' + line)
        output.write('\t<\segment>\n\n')
    output.write('<\entry>')
"""
if __name__ == '__main__':                # call if module is called as main
    main()

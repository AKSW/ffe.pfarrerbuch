import xml.etree.ElementTree as ElementTree
from vicar import Vicar
from segmentAnalyzer import SegmentAnalyzer
import xml.dom.minidom as minidom
import sys

class Writer:
    def __init__(self):
        self.root = ElementTree.Element('file')

    def fromParser(self, parser):
        self.parser = parser
        i = 0
        for segment in parser.segmentation(parser.readInputFile()):
            try:
                vicar = Vicar(i)
                vicar.original = segment
                analyzer = SegmentAnalyzer(segment, vicar)
                analyzer.createEntry(self.root)
            except Exception as err:
                sys.stderr.write('segment number: %s\n' % str(i))
                sys.stderr.write('ERROR: %s\n' % str(err))
                sys.stderr.write('in segment: %s\n' % segment)
            i = i + 1


    def dumpToFile(self, outputFile):
        xmlString = ElementTree.tostring(self.root, encoding="unicode")
        xml = minidom.parseString(xmlString)
        prettyString = xml.toprettyxml()
        output = open(outputFile, 'w+')
        output.write(prettyString)
        output.close
        #tree.write(outputFile)

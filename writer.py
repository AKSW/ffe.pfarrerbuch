import xml.etree.ElementTree as ElementTree
from vicar import Vicar
from segmentAnalyzer import SegmentAnalyzer
import xml.dom.minidom as minidom

class Writer:
    def __init__(self):
        self.root = ElementTree.Element('file')

    def fromParser(self, parser):
        self.parser = parser
        i = 0
        for segment in parser.segmentation(parser.readInputFile()):
            vicar = Vicar(i)
            vicar.rawData = segment
            analyzer = SegmentAnalyzer(segment, vicar)
            analyzer.createEntry(self.root)
            i = i + 1

    def dumpToFile(self, outputFile):
        xmlString = ElementTree.tostring(self.root, encoding="unicode")
        xml = minidom.parseString(xmlString)
        prettyString = xml.toprettyxml()
        output = open(outputFile, 'w+')
        output.write(prettyString)
        output.close
        #tree.write(outputFile)
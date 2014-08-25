#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parser module which is relevant to parse a rawtext-file into a specific
XML - Format
Author: Robert R.
Version: 1.0

This file is the main-file and should be called as main in order to parse
a certain document

The project can be altered to fit for different needs

format convention of the raw-text:
    - name should be always in the first line of a new entry
    - no headers
    - no frontpages or other text besides the entries
    - first line should be the name / entry of the first vicar
    - each entry need to be seperated with a new line

bugs:
    list if any are found

to-do:
    add date inaccuracy in analyzeDate in segmentAnalyzer
"""

import sys
import getopt
from writer import Writer


class Parser:

    def __init__(self, fileName):
        self.filename = fileName

    def readInputFile(self):              # reads the input file
        f = open(self.filename, 'r', encoding="utf8")
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
            if count == 0 and line == "\n":
                segments.append(segment[:])
                segment[:] = []
                count = 1
            elif count == 1 and line != "\n":
                buf = line
                count = 2
            elif count == 2 and "Ord.:" in line:
                segment.append(buf)
                segment.append(line)
                count = 0
            elif count == 2:
                count = 1
            elif count == 0:
                segment.append(line)
        return segments


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:o:", ["input", "output"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-i", "--input"):
            inputFile = a
        elif o in ("-o", "--output"):
            outputFile = a

    Parser(inputFile)
    writer = Writer()
    writer.fromParser(outputFile)
    # TODO implement dumping to stdout
    writer.dumpToFile("output.xml")


def usage():
    print("""
Please use the following options:
    -i  --input     The input file
    -o  --output    The output file (optional). If not present, the output is written to stdout
""")

if __name__ == '__main__':                # call if module is called as main
    main(sys.argv[1:])

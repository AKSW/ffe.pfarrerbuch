default:
	python3 parser.py -i io/ungarn-input.txt -o outputText.xml
	xsltproc parserXMLtoRDF.xsl outputText.xml > ungarisch.rdf
	rapper -i 'rdfxml' -o turtle ungarisch.rdf > ungarisch.ttl

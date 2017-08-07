FFE Pfarrerbuch
===============
This is a flat file extractor (ffe) for in the end generating RDF to be used by the pfarrerbuch project.

The input is comming from Word files of our hungarian partner.

# Preparation

Install [AltSearch](https://extensions.libreoffice.org/extensions/alternative-dialog-find-replace-for-writer) for you LibreOffice.
Insert a linebreak after each pagebreak, search for "`\m`" insert "`\m\n`".
(Because there is one person per page and thus in a later stage we need to identify page breaks).

# Convert doc to plain text (io)
The content of the word documents needs to be converted to plain text using the script in `io/doc2io.sh`

    $ cd io
    $ ./doc2iop.sh <list all the word files here>

This produces a file called `io/ungarn-input.txt` which serves as input for the next step.

# Parse values from plain text and write to RDF

Go to the top level and run `make`.

The result should be in `ungarisch.ttl`.

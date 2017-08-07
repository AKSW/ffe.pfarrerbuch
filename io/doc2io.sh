#!/bin/sh

input=$@
output='ungarn-input.txt'
tmp='tmp.txt'
tmp2='tmp2.txt'

echo '' > ${output}

for file in ${input}
do
    echo "${file} …"
    antiword -w 0 "${file}" > ${tmp}
    sed 's/∞/8/g' ${tmp} > ${tmp2}
    sed 's/\([0-9]*\)\. \([0-9]*\)/\1.\2/g' ${tmp2} >> ${output}
    vim -c '%s/\(\n\)\+Ord.:/\rOrd.:/g' -c 'write' -c 'quit' ${output}
done

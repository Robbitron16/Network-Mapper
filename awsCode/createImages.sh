#!/bin/bash
input="./test.txt"

while IFS= read -r line
do
    fields=($line)
    filename=${fields[0]}
    addrspace=${fields[1]}
    python parse.py results.txt $filename True $addrspace
done <"$input"

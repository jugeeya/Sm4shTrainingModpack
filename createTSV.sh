#!/bin/bash

FIGHTERDIRS=AllFighterData/*
rm -r TSV
mkdir TSV
for f in $FIGHTERDIRS
do
    tsvName=$(basename $f).tsv
    echo "Processing for TSV/$tsvName..."
    python3 kuroganeParser.py $(basename $f) > TSV/$tsvName
done

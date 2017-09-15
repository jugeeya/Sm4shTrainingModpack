#!/usr/bin/env bash

allChars=$1
folder=$2
scripts="script*.txt"
if [ $1 == "all" ]
then
    allChars=../../AllFighterData/*
fi
rm -r output
for dir in $allChars
do
    char=$(basename $dir)
    echo "Disassembling $char..."
    mkdir -p ../../AllFighterMSCCompiled/$char/script/msc
    python3 disasm.py ../../AllFighterData/$char/script/msc/$char.mscsb
    if [ $# -eq 2 ]
    then
	for script in $folder/*
	do
	    echo "Moving $script..."
	    rm output/$(basename $script)
	    cp $script output/$(basename $script)
	done
    fi
    if [ $char == "rockman"  ]
    then
	echo "Moving script_2324.txt..."
	rm output/script_2324.txt
	cp scriptFolders/rockmanFix/script_2324.txt output/script_2324.txt
    fi
    cd output
    echo "Reassembling $char..."
    python3 ../asm.py
    echo "Moving to AllFighterMSCCompiled..."
    mv test.mscsb ../../../AllFighterMSCCompiled/$char/script/msc/$char.mscsb
    cd ..
    # rm -r output
done

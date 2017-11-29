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
    python3 disasm.py --char-std ../../AllFighterData/$char/script/msc/$char.mscsb
    if [ $# -eq 2 ]
    then
	for script in $folder/*
	do
	    scriptBasename=$(basename $script)
	    if [ ${scriptBasename:0:6} == "script" ]
	    then
		echo "Replacing $script..."
		rm output/$scriptBasename
	    else
		echo "Adding $script..."
		echo $scriptBasename >> output/Scripts
	    fi
	    cp $script output/$scriptBasename
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

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
		if [ $char == "rockman" ] && [ $scriptBasename == "script_2239.txt" ]
		then
		    echo "Not replacing script_2239..."
		else
		    echo "Replacing $script..."
		    rm output/$scriptBasename
		fi
	    else
		echo "Adding $script..."
		echo $scriptBasename >> output/Scripts
	    fi
	    if [ $char == "rockman" ] && [ $scriptBasename == "script_2239.txt" ]
	    then
		echo "Mega Man sucks. Not removing 2239..."
	    else
		cp $script output/$scriptBasename
	    fi
	done
    fi
    if [ $char == "rockman"  ]
    then
	echo "Moving script_2324.txt..."
	rm output/script_2324.txt
	cp scriptFolders/rockmanFix/script_2324.txt output/script_2324.txt
	echo "Moving script_2241.txt..."
	rm output/script_2241.txt
	cp scriptFolders/rockmanFix/script_2241.txt output/script_2241.txt
    fi
    if [ $char == "szerosuit"  ]
    then
	echo "Moving script_2239.txt..."
	rm output/script_2239.txt
	cp scriptFolders/szerosuitFix/script_2239.txt output/script_2239.txt
    fi
    cd output
    echo "Reassembling $char..."
    python3 ../asm.py
    echo "Moving to AllFighterMSCCompiled..."
    mv test.mscsb ../../../AllFighterMSCCompiled/$char/script/msc/$char.mscsb
    cd ..
    # rm -r output
done

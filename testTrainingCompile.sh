#!/bin/bash

charName=$1
weaponName=$2
if [ $2 == "body" ]
then
    ./FITD.exe -o $1bodyInput -m AllFighterData/$1/motion AllFighterData/$1/script/animcmd/body/motion.mtable
    mkdir -p $1bodyOutput/animcmd
    if [ $3 == "nothing" ]
    then
	for f in $1bodyInput/animcmd/*
	do
	    fbasename=$(basename $f)
            echo "Processing file (initial movement) $(basename $f)..."
	    cp $f $1bodyOutput/animcmd/$(basename $f)
	done
    fi
    if [ $3 != "nothing" ]
    then
	for f in $1bodyInput/animcmd/$3
	do
	    fbasename=$(basename $f)
	    if [ $(python3 stretchChecker.py $1 $2 $fbasename) == "blacklisted" ]
	    then
		echo "Processing blacklisted file $f for $1..."
		python3 gameToEffectScript.py $f ty > $1bodyOutput/animcmd/$(basename $f)
	    else
		echo "Processing file $f for $1..."
		python3 gameToEffectScript.py $f t > $1bodyOutput/animcmd/$(basename $f)
	    fi
	done
    fi
    mv $1bodyInput/fighter.mlist $1bodyOutput/fighter.mlist
    ./FITC.exe -o $1bodyCompiled $1bodyOutput/fighter.mlist
else
    ./FITD.exe -o $1weapon$2Input -m AllFighterData/$1/motion AllFighterData/$1/script/animcmd/weapon/$2/motion.mtable
    mkdir -p $1weapon$2Output/animcmd
    for f in $1weapon$2Input/animcmd/*
    do
	fbasename=$(basename $f)
	echo "Processing file (initial movement) $(basename $f)..."
	cp $f $1weapon$2Output/animcmd/$(basename $f)
    done
    if [ $3 != "nothing" ]
    then
	for f in $1weapon$2Input/animcmd/$3
	do
	    fbasename=$(basename $f)
	    echo "Processing file $(basename $f)..."
	    python3 gameToEffectScript.py $f t > $1weapon$2Output/animcmd/$(basename $f)
	done
    fi
    mv $1weapon$2Input/fighter.mlist $1weapon$2Output/fighter.mlist
    ./FITC.exe -o $1weapon$2Compiled $1weapon$2Output/fighter.mlist
fi




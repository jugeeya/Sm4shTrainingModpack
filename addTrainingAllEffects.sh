#!/bin/bash

FIGHTERDIRS=AllFighterData/*
rm -r AllFighterDataCompiledTraining || true
mkdir AllFighterDataCompiledTraining
for d in $FIGHTERDIRS
do
    dbasename=$(basename $d)
    if [ $dbasename != "reflet" ] && [ $dbasename != "koopajr" ] && [ $dbasename != "sonic" ]
    then
	    ./addTrainingMultCharProjct.sh $(basename $d)
    fi
done

#!/bin/bash

FIGHTERDIRS=AllFighterData/*
rm -r AllFighterDataCompiled || true
mkdir AllFighterDataCompiled
for d in $FIGHTERDIRS
do
    dbasename=$(basename $d)
    if [ $dbasename != "reflet" ] && [ $dbasename != "koopajr" ] && [ $dbasename != "sonic" ]
    then
	    ./addMultCharProjct.sh $(basename $d)
    fi
done

#!/bin/bash

FIGHTERDIRS=AllFighterData/*
rm -r AllFighterDataCompiled || true
mkdir AllFighterDataCompiled
for d in $FIGHTERDIRS
do
    dbasename=$(basename $d)
    #if [ $dbasename != "bayonetta" ] && [ $dbasename != "dedede" ] && [ $dbasename != "kirby" ] && [ $dbasename != "gamewatch" ] && [ $dbasename != "palutena" ]
    #then
    if [ $dbasename != "mewtwo" ] && [ $dbasename != "murabito" ] && [ $dbasename != "reflet" ] && [ $dbasename != "sonic" ] && [ $dbasename != "yoshi" ] && [ $dbasename != "koopajr" ]
    then
	./addOneCharProjct.sh $(basename $d)
    fi
    #fi
done

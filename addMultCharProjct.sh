#!/bin/bash

allChars="$@"
for c in $allChars
do
    dbasename=$c
    d=AllFighterData/$dbasename
    ./FITD.exe -o $(basename $d)bodyInput -m $d/motion $d/script/animcmd/body/motion.mtable
    WEAPONS=AllFighterData/$dbasename/script/animcmd/weapon/*
    for w in $WEAPONS
    do
	if [[ -f $w/motion.mtable && $(basename $w) != "clayrocket" ]]
	then ./FITD.exe -o $(basename $d)$(basename $w)Input -m $d/motion $d/script/animcmd/weapon/$(basename $w)/motion.mtable
	fi	
    done
    INPUTDIRS=$(basename $d)*Input
    for i in $INPUTDIRS
    do
	FILES=$i/animcmd/*.acm
	mkdir -p ${i::-5}Output
	mkdir -p ${i::-5}Output/animcmd
	mv $i/fighter.mlist ${i::-5}Output/fighter.mlist
	
	for f in $FILES
	do
	    fbasename=$(basename $f)
	    bodyWeaponName=${i:${#dbasename}:-5}
	    if [ $(python3 stretchChecker.py $dbasename $bodyWeaponName $fbasename) == "blacklisted" ]
	    then
		echo "Processing blacklisted file $f for $(basename $d)..."
	        python3 gameToEffectScript.py $f y > ${i::-5}Output/animcmd/$(basename $f)
	    else
		echo "Processing file $f for $(basename $d)..."
		python3 gameToEffectScript.py $f > ${i::-5}Output/animcmd/$(basename $f)
	    fi
	done
      
	./FITC.exe -o AllFighterDataCompiled/${i::-5}Compiled ${i::-5}Output/fighter.mlist
	rm -r $i
	rm -r ${i::-5}Output

	d2=AllFighterDataCompiled/${i::-5}Compiled
	echo "Moving from folder $(basename $d2)..."
	charFolder=AllFighterDataCompiled/$dbasename
	#rm -r $charFolder
	mkdir -p $charFolder
	mkdir -p $charFolder/script
	mkdir -p $charFolder/script/animcmd
	if [ ${i:${#dbasename}:-5} == "body" ]
	then
	    mkdir -p $charFolder/script/animcmd/body
	    cp $d2/effect.bin $charFolder/script/animcmd/body/effect.bin
	else
	    mkdir -p $charFolder/script/animcmd/weapon
	    weaponName=${i:${#dbasename}:-5}
	    mkdir -p $charFolder/script/animcmd/weapon/$weaponName
	    cp $d2/effect.bin $charFolder/script/animcmd/weapon/$weaponName/effect.bin
	fi
	rm -r $d2
    done
done

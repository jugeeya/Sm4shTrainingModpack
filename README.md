# Sm4shTrainingModpack

## What This Is

This is the combination of scripts that I use to create the Hitbox Visualization / Training Modpack found at http://gamebanana.com/gamefiles/5750. The following information is how to recreate the same data and even change its behavior as desired. Note that the character arguments are all in terms of the game's name of the characters (so "mario" for Mario, "purin" for Jigglypuff, and so on).

## Requirements

First and foremost, a dump of the game is needed. More specifically, a folder MUST be placed in this directory entitled "AllFighterData" which includes the 58 character folders found in data/fighter of the game dump. It is from this folder that all the scripts find the game's data.

## addAllEffects.sh

Upon running this command, every fighter will be compiled based on the data in AllFighterData and the output (in the form of effect.bin files in the correct directory) will be placed in a new folder entitled AllFighterDataCompiled. This essentially contains the unpacked contents of data/fighter. From this output folder, the character folders can be dragged into Sm4shexplorer's data/fighter at which point the modpack can be packed.

## addMultCharProjct.sh

addAllEffects.sh uses this to compile all the characters by calling it one character at a time. However, this script can also be used to add any number of specific characters (along with their weapons) by using them as arguments as such: 

```
# compile mario, bowser, and lucario to the AllFighterDataCompiled folder
./addMultCharProjct.sh mario koopa lucario
```

## gameToEffectScript.py
This is the core of all the work in these scripts. Given a game file (.acm), a character's TSV file (if the file is in the character's body), and whether or not it is blacklisted, this script will output the exact same game script with the effect.bin portion changed based on a variety of factors. It parses the game.bin portion to create the effect.bin portion that generates the hitbox and overlay visualizations. didHandleEdgeCase() is a special function that contains tons of lines of code for edge cases that cannot be handled by the script due to the acm files not containing enough information. 

```
# output a normal move's new .acm file given its directory is correctly formatted
python3 gameToEffectScript.py marthbodyInput/animcmd/AttackAirF.acm
# output a blacklisted move's new .acm file given its directory is correctly formatted ('y' argument at end)
python3 gameToEffectScript.py yoshibodyInput/animcmd/AttackLw3.acm y
```

## createTSV.sh
Calls kuroganeParser.py on every character in AllFighterData and creates a tsv file for them in the folder TSV/. Necessary for addMultCharProjct.sh. The current commit's TSV files will always be up-to-date, so this need only be called if kuroganeParser.py is changed.

## kuroganeParser.py
Parses kuroganehammer.com through HTML parsing and then by using FrannDotExe's API to create one character's TSV file of data. 

## stretchChecker.py 
Uses the blacklist.tsv in blacklist/ to find out if a move is blacklisted and should therefore be processed differently. 

## testCompile.sh
Used to test compilations on single characters quickly, with an argument to only compile specific moves (using regex). Very useful for finding out which moves are causing a problem. The raw decompiled files will be in ($charName)bodyInput/animcmd/, the midpoint files that are processed by gameToEffectScript.py are in ($charName)bodyOutput/animcmd/, and the output .bin files given by FITC are in ($charName)bodyCompiled.

```
# called as such: ./testCompile.sh charName "body"/weaponName moveNamesRegex
# compile all of Ike's normals
./testCompile.sh ike body Attack*.acm
# compile all of Duck Hunt's can's specials
./testCompile.sh duckhunt can Special*.acm
# can also be used to test raw decompilation and compilation for FITX, or to simply get the files to read/edit
# done using argument "nothing"
./testCompile.sh peach body nothing
```

## convertToAddEffect.py
Used in conjunction with testCompile.sh in order to get code that will work with gameToEffectScript.py's didHandleEdgeCase() function. Takes the effect.bin portion of a processed .acm file and outputs "addEffect()" lines that can be copy-pasted into the conditionals of the didHandleEdgeCase() function.

## FITC, FITD, and SALT
These are included because the current version of FITX is crucial to the performance of the scripts, as some bugs greatly affect a good few characters. 

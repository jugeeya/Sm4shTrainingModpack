# Sm4shTrainingModpack

## What This Is

This is the combination of scripts that I use to create the Hitbox Visualization / Training Modpack found at http://gamebanana.com/gamefiles/5750. The following information is how to recreate the same data and even change its behavior as desired. Note that the character arguments are all in terms of the game's name of the characters (so "mario" for Mario, "purin" for Jigglypuff, and so on).

## Requirements

First and foremost, a dump of the game is needed. More specifically, a folder MUST be placed in this directory entitled "AllFighterData" which includes the 58 character folders found in data/fighter of the game dump. It is from this folder that all the scripts find the game's data.
The whole workspace should look like:

```
-this_repository/
    -AllFighterData/
        -bayonetta/
        ...
        -zelda/
    -blacklist/
    -TSV/
    -edgeCaseCode/
    -all_other_python_scripts_and_FITX_exes
```
## Compiling all characters game-wide

```
python3 performCompilation.py all
```

Upon running this command, every fighter will be compiled based on the data in AllFighterData and the output (in the form of effect.bin files in the correct directory) will be placed in a new folder entitled AllFighterDataCompiled. This essentially contains the unpacked contents of data/fighter. From this output folder, the character folders can be dragged into Sm4shexplorer's data/fighter at which point the modpack can be packed.

## Compiling all characters training-mode-only

```
python3 performCompilation.py training all
```

The same as the previous command, but produces training-mode-only output: the hitboxes will only be shown in Training Mode, and elsewhere the original effect.bin will be displayed. The output will be placed in a new folder entitled AllFighterDataCompiledTraining, again in the form of data/fighter.

## Compiling any number of characters game-wide

```
# compile mario, bowser, and lucario to the AllFighterDataCompiled folder
python3 performCompilation.py mario koopa lucario
```

The script can also be used to add any number of specific characters (along with their weapons) by using them as arguments as shown above.

## Compiling any number of characters training-mode-only

```
# compile peach, dark pit, and corrin to the AllFighterDataCompiledTraining folder
python3 performCompilation.py training peach pitb kamui
```

Again, same as the previous but produces training-mode-only output in the corresponding folder.

## Where processing occurs
#### *processFile(filePath, isBlacklisted=False, isTrainingOnly=False)*
<<<<<<< HEAD
This is the core of all the work in the script. Given a game file (.acm), a character's TSV file (if the file is in the character's body), and whether or not it is blacklisted, this method will output the exact same game script with the effect.bin portion changed based on a variety of factors. It parses the game.bin portion to create the effect.bin portion that generates the hitbox and overlay visualizations. didHandleEdgeCase() is a special function that checks the edgeCaseCode/ folder for specific .acm files that cannot be handled by the script due to the acm files not containing enough information.
=======
This is the core of all the work in the script. Given a game file (.acm), a character's TSV file (if the file is in the character's body), and whether or not it is blacklisted, this method will output the exact same game script with the effect.bin portion changed based on a variety of factors. It parses the game.bin portion to create the effect.bin portion that generates the hitbox and overlay visualizations. *didHandleEdgeCase()* is a special function that contains tons of lines of code for edge cases that cannot be handled by the script due to the acm files not containing enough information.
>>>>>>> 956fca14c6507e614ed329647affeaefea624e17

```
# in Python3
# returns a string containing a normal move's new .acm file given its directory is correctly formatted
processFile("marthbodyInput/animcmd/AttackAirF.acm")
# returns a string containing a blacklisted move's new .acm file given its directory is correctly formatted
processFile("yoshibodyInput/animcmd/AttackLw3.acm", isBlacklisted=True)
```

#### *stretchChecker(char, bodyOrWeapon, move)* 
Uses the blacklist.tsv in blacklist/ to find out if a move is blacklisted and should therefore be processed differently. 
Returns one of three strings:
* "okay", the move should be processed normally
* "blacklisted", the move should be processed without adding hitbox effects
* "noprocess", the move should simply be placed in the output directory as given

## createTSV.py
This script creates a tsv file for them in the folder TSV/ for all characters in AllFighterData. Necessary for peformCompilation.py. The current commit's TSV files will always be up-to-date, so this need only be called if *parseChar()* is changed.

#### *parseChar(charName)*
Parses www.kuroganehammer.com through HTML parsing and then by using FrannDotExe's API https://github.com/Frannsoft/FrannHammer to create one character's TSV file of data. 

## Testing compilation and viewing output scripts
Used to test compilations on single characters quickly, with an argument to only compile specific moves (using regex). Very useful for finding out which moves are causing a problem. The raw decompiled files will be in ($charName)("body"/$weaponName)Input/animcmd/, the midpoint files that are processed by *parseChar()* are in ($charName)("body"/$weaponName)Output/animcmd/, and the output .bin files given by FITC are in ($charName)("body"/$weaponName)Compiled.

```
<<<<<<< HEAD
# python3 performCompilation.py test charName "body"/weaponName moveNamesRegex
=======
# called as such: python3 performCompilation.py test charName "body"/weaponName moveNamesRegex
# compile all of Little Mac's moves
python3 performCompilation.py test littlemac body *.acm

>>>>>>> 956fca14c6507e614ed329647affeaefea624e17
# compile all of Ike's normals
python3 performCompilation.py test ike body Attack*.acm
# outputs ikebodyInput/, ikebodyOutput/, and ikebodyCompiled/

# compile all of Duck Hunt's can's specials
python3 performCompilation.py test duckhunt can Special*.acm
# outputs duckhuntcanInput/, duckhuntcanOutput/, and duckhuntcanCompiled/

# can also be used to test raw decompilation and compilation for FITX, or to simply get the files to read/edit
# done using argument "nothing"
python3 performCompilation.py test peach body nothing
# outputs peachbodyInput/, peachbodyOutput/, and peachbodyCompiled/
```

## Testing training compilation
```
# python3 performCompilation.py testTraining charName "body"/weaponName moveNamesRegex
```
Same as the previous, but produces training-mode-only output.

<<<<<<< HEAD
## handleEdgeCaseCode.py
Used in conjunction with test compilations in order to place an edited script into the edgeCaseCode/ folder for the *didHandleEdgeCase()* function.
=======
## convertToAddEffect.py
```
python3 convertToAddEffect.py rockmanbodyOutput/animcmd/SpecialHi.acm > megaManUpBEdgeCaseCode.txt
```
Used in conjunction with test compilations in order to get code that will work with performCompilation.py's *didHandleEdgeCase()* function. Takes the effect.bin portion of a processed .acm file and outputs *addEffect()* lines that can be copy-pasted into the conditionals of the didHandleEdgeCase() function.
>>>>>>> 956fca14c6507e614ed329647affeaefea624e17

## FITC, FITD, and SALT
These are included because the current version of FITX is crucial to the performance of the scripts, as some bugs greatly affect a good few characters. 

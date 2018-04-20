# Sm4shTrainingModpack

## What This Is

This is the combination of scripts that I use to create the Hitbox Visualization / Training Modpack found at http://gamebanana.com/gamefiles/5750. The following information is how to recreate the same data and even change its behavior as desired. Note that the character arguments are all in terms of the game's name of the characters (so "mario" for Mario, "purin" for Jigglypuff, and so on).

## Requirements

First and foremost, a dump of the game is needed. More specifically, a folder MUST be placed in this directory entitled "AllFighterData" which includes the 58 character folders found in data/fighter of the game dump. An easy way to get this would be to open Sm4shexplorer and to right-click and extract the data/fighter folder, after which you can find the folders in [your_sm4sh_explorer_folder]/extract/data/fighter/. Be sure to only have the 58 playable non-final smash characters. 

It is from this folder that all the scripts find the game's data.
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
# Hitbox Effects Portion (ACMD, using FITX)
## Compiling all characters game-wide

```
python3 performCompilation.py all
```

Upon running this command, every fighter will be compiled based on the data in AllFighterData and the output (in the form of effect.bin files in the correct directory) will be placed in a new folder entitled AllFighterDataCompiled. This essentially contains the unpacked contents of data/fighter. From this output folder, the character folders can be dragged into Sm4shexplorer's data/fighter at which point the modpack can be packed.

*Please note that this command currently does not compile all characters due to a bug in FITX that causes decompilation errors for 'koopajr' and 'reflet'. Therefore, to actually compile all characters, run the command above and once it finishes, also call ```python3 performCompilation.py koopajr reflet```. During this compilation, simply click "Close the program" on the FITD errors that occur. This simply means that some moves for these two characters are not processed.*

## Compiling all characters training-mode-only

```
python3 performCompilation.py training all
```

The same as the previous command, but produces training-mode-only output: the hitboxes will only be shown in Training Mode, and elsewhere the original effect.bin will be displayed. The output will be placed in a new folder entitled AllFighterDataCompiledTraining, again in the form of data/fighter.

*The note from above for non-training-mode-only applies here as well. Simply call ```python3 performCompilation.py training koopajr reflet``` instead.* 

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
#### *processFile(isBlacklisted=False, isTrainingOnly=False)*
This is the core of all the work in the script. Given an ACMFile object, a character's TSV file (if the file is in the character's body), and whether or not it is blacklisted, this method will output the exact same game script with the effect.bin portion changed based on a variety of factors. It parses the game.bin portion to create the effect.bin portion that generates the hitbox and overlay visualizations. *didHandleEdgeCase()* is a special function that checks the edgeCaseCode/ folder for specific .acm files that cannot be handled by the script due to the acm files not containing enough information.  

#### Testing a single file
To call this function and inspect how it processes single files, it can be called as shown below:


```
# python3 performCompilation.py acmFilePath isBlacklistedAndOrTrainingOnly
# the isBlacklistedAndOrTrainingOnly argument can be 'b', 't', or 'tb' for blacklisted, training-mode-only, or both, respectively
# prints normal move's new .acm file given its directory is correctly formatted
python3 performCompilation.py marthbodyInput/animcmd/AttackAirF.acm
# prints a blacklisted move's new .acm file given its directory is correctly formatted
python3 performCompilation.py yoshibodyInput/animcmd/AttackLw3.acm b
```

#### *stretchChecker(char, bodyOrWeapon, move)* 
Uses the blacklist.tsv in blacklist/ to find out if a move is blacklisted and should therefore be processed differently. 
Returns one of three strings:
* "okay", the move should be processed normally
* "blacklisted", the move should be processed without adding hitbox effects
* "noprocess", the move should simply be placed in the output directory as given

## *createTSV.py*
This script creates a tsv file for them in the folder TSV/ for all characters in AllFighterData. Necessary for peformCompilation.py. The current commit's TSV files will always be up-to-date, so this need only be called if *parseChar()* is changed.

#### *parseChar(charName)*
Parses www.kuroganehammer.com through HTML parsing and then by using FrannDotExe's API https://github.com/Frannsoft/FrannHammer to create one character's TSV file of data. 

## Testing compilation and viewing output scripts
Used to test compilations on single characters quickly, with an argument to only compile specific moves (using regex). Very useful for finding out which moves are causing a problem. The raw decompiled files will be in ($charName)("body"/$weaponName)Input/animcmd/, the midpoint files that are processed by *parseChar()* are in ($charName)("body"/$weaponName)Output/animcmd/, and the output .bin files given by FITC are in ($charName)("body"/$weaponName)Compiled.

```
# python3 performCompilation.py 'test' charName "body"/weaponName moveNamesRegex
# compile all of Little Mac's moves
python3 performCompilation.py test littlemac body *.acm
# outputs littlemacbodyInput/, littlemacbodyOutput/, and littlemacbodyCompiled/

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

## *handleEdgeCaseCode.py*
Used in conjunction with test compilations in order to place an edited script into the edgeCaseCode/ folder for the *didHandleEdgeCase()* function.


## FITC, FITD, and SALT
These are included because the current version of FITX is crucial to the performance of the scripts, as some bugs greatly affect a good few characters. 

# Toggle Effects (MSC, using PyMSC)
## Compiling certain all characters (for both game-wide and training-mode-only)
In the pymsc/pymsc folder, 

```
python3 createMSCs.py charName pathToEditedMSCScriptsFolder
```

Upon running this command, every fighter will be compiled based on the data in AllFighterData and the output (in the form of \[charName\].mscsb files in the correct directory) will be placed in a new folder entitled AllFighterMSCCompiled. This essentially contains the remainder of the unpacked contents of data/fighter. From this output folder, the character folders can be dragged into Sm4shexplorer's data/fighter at which point the modpack can be packed.

import os, sys, struct, subprocess, shlex, glob, shutil, math
from ACMFile import ACMFile
from collections import OrderedDict

def stretchChecker(char, bodyOrWeapon, move):
    charName = char
    bodyWeaponName = bodyOrWeapon
    moveName = move

    with open("blacklist/blacklist.tsv", newline="\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    inChar = False
    inBodyWeapon = False
    foundCharAndMove = False

    for i in lines:
        if i.startswith(moveName):
            return "noprocess"
        if i.startswith(charName):
            inChar = True
        elif (i[0] == "\t" and inChar == True):
            if (i[1:] == bodyWeaponName):
                inBodyWeapon = True
            elif (i[0:2] == "\t\t" and inBodyWeapon == True):
                if (i[2:] == moveName or i[2:] == "*"):
                    return "blacklisted"
            else:
                inBodyWeapon = False
        else:
            inChar = False

    if (foundCharAndMove == False):
        return "okay"

def main():
    charList = []
    noprocessWeapons = ["clayrocket", "can", "clay", "reticle", "sunbullet", "dein", "dein_s", "phantom"]
    if len(sys.argv) >= 2 and (sys.argv[1] in {"test", "testTraining", "testCustom"}):
        processList = []
        if len(sys.argv) != 5:
            print("testing requires exactly 4 arguments: \'test\'/\'testTraining\', char, bodyOrWeapon, movesToCompile")
            exit()
        trainingMode = False
        if sys.argv[1] == "testTraining":
            trainingMode = True
        char = sys.argv[2]
        bodyOrWeapon = sys.argv[3]
        weaponBool = False if bodyOrWeapon == "body" else True
        movesToCompile = sys.argv[4]
        inputDir = "{}{}Input".format(char, bodyOrWeapon)
        outputDir = "{}{}Output".format(char, bodyOrWeapon)
        compiledDir = "{}{}Compiled".format(char, bodyOrWeapon)
        if bodyOrWeapon == "body":
            subprocess.run(shlex.split("./FITD.exe -o {} -m AllFighterData/{}/motion AllFighterData/{}/script/animcmd/body/motion.mtable".format(inputDir, char, char)))
        else:
            subprocess.run(shlex.split("./FITD.exe -o {} -m AllFighterData/{}/motion AllFighterData/{}/script/animcmd/weapon/{}/motion.mtable".format(inputDir, char, char, bodyOrWeapon)))
        os.makedirs("{}/animcmd".format(outputDir), exist_ok=True)
        files = os.listdir("{}/animcmd/".format(inputDir))
        for file in files:
            print("Moving file {}...".format(file))
            shutil.copy("{}/animcmd/{}".format(inputDir, file), "{}/animcmd/{}".format(outputDir, file))
        if movesToCompile != "nothing":
            files = glob.glob("{}/animcmd/{}".format(inputDir, movesToCompile))
            specificEffectLines = ["", ""]
            for filePath in files:
                file = os.path.basename(filePath)
                stretchCheck = stretchChecker(char, bodyOrWeapon, file)
                if stretchCheck == "blacklisted":
                    print("Processing blacklisted file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    currFile = ACMFile(filePath, specificEffectLines[0], specificEffectLines[1])
                    outputFile.write(currFile.processFile(isBlacklisted=True, isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    specificEffectLines = currFile.getSpecificEffectLines()
                    outputFile.close()
                else:
                    print("Processing file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    currFile = ACMFile(filePath, specificEffectLines[0], specificEffectLines[1])
                    outputFile.write(currFile.processFile(isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    specificEffectLines = currFile.getSpecificEffectLines()
                    outputFile.close()
                '''
                elif stretchCheck == "noprocess":
                    print("Moving noprocess file {} for {}...".format(file, char))
                    shutil.copy(filePath, "{}/animcmd/{}".format(outputDir, file))
                '''
        os.rename("{}/fighter.mlist".format(inputDir), "{}/fighter.mlist".format(outputDir))
        subprocess.run(shlex.split("./FITC.exe -o {} {}/fighter.mlist".format(compiledDir, outputDir)))
        exit()

    charStartIndex = 1
    trainingMode = False
    allChars = os.listdir("AllFighterData/")
    decompileErrorChars = ['koopajr', 'reflet'] # not on latest commit, but it has a problem with conditionals
    for char in decompileErrorChars:
        allChars.remove(char)
    if len(sys.argv) >= 2 and sys.argv[1] == "training":
        charStartIndex = 2
        trainingMode = True
        if len(sys.argv) >= 3 and sys.argv[2] == "all":
            charList = allChars
        else:
            for argIndex in range(charStartIndex, len(sys.argv)):
                charList.append(sys.argv[argIndex])
    elif len(sys.argv) >= 2 and sys.argv[1] == "all":
        charList = allChars
    else:
        for argIndex in range(charStartIndex,len(sys.argv)):
            charList.append(sys.argv[argIndex])
    for char in charList:
        subprocess.run(shlex.split("./FITD.exe -o {}bodyInput -m AllFighterData/{}/motion AllFighterData/{}/script/animcmd/body/motion.mtable".format(char,char,char)))
        if not trainingMode:
            if os.path.isdir("AllFighterData/{}/script/animcmd/weapon".format(char)):
                weapons = os.listdir("AllFighterData/{}/script/animcmd/weapon".format(char))
                for weapon in weapons:
                    weaponPath = "AllFighterData/{}/script/animcmd/weapon/{}".format(char, weapon)
                    if os.path.isfile("{}/motion.mtable".format(weaponPath)) and weapon not in noprocessWeapons:
                        subprocess.run(shlex.split("./FITD.exe -o {}{}Input -m AllFighterData/{}/motion {}/motion.mtable".format(char, weapon, char, weaponPath)))

        inputDirectories = glob.glob("{}*Input".format(char))
        for inputDir in inputDirectories:
            outputDir = inputDir[:-5] + "Output"
            os.makedirs("{}/animcmd".format(outputDir), exist_ok=True)
            os.rename("{}/fighter.mlist".format(inputDir), "{}/fighter.mlist".format(outputDir))
            bodyOrWeapon = inputDir[len(char):-5]
            weaponBool = False if bodyOrWeapon == "body" else True
            files = os.listdir("{}/animcmd".format(inputDir))
            specificEffectLines = ["", ""]
            for file in files:
                filePath = "{}/animcmd/{}".format(inputDir, file)
                stretchCheck = stretchChecker(char, bodyOrWeapon, file)
                if stretchCheck == "blacklisted":
                    print("Processing blacklisted file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    currFile = ACMFile(filePath, specificEffectLines[0], specificEffectLines[1])
                    outputFile.write(currFile.processFile(isBlacklisted=True, isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    specificEffectLines = currFile.getSpecificEffectLines()
                    outputFile.close()
                elif stretchCheck == "noprocess":
                    print("Moving noprocess file {} for {}...".format(file, char))
                    shutil.copy(filePath, "{}/animcmd/{}".format(outputDir, file))
                else:
                    print("Processing file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    currFile = ACMFile(filePath, specificEffectLines[0], specificEffectLines[1])
                    outputFile.write(currFile.processFile(isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    specificEffectLines = currFile.getSpecificEffectLines()
                    outputFile.close()
                    if char == "bayonetta" and file == "SpecialAirHi.acm":
                        shutil.copy("edgeCaseCode/bayonettabodySpecialAirHi.acm", "{}/animcmd/{}".format(outputDir, file))
                        print("Copying special edge case for bayonetta...")

            compiledDir = "AllFighterDataCompiled/{}Compiled".format(inputDir[:-5])
            if trainingMode:
                compiledDir = "AllFighterDataCompiledTraining/{}Compiled".format(inputDir[:-5])
            subprocess.run(shlex.split("./FITC.exe -o {} {}/fighter.mlist".format(compiledDir, outputDir)))
            shutil.rmtree(inputDir, ignore_errors=True)
            shutil.rmtree(outputDir, ignore_errors=True)
            print("Moving to folder {}...".format(compiledDir))
            if bodyOrWeapon == "body":
                finalDir = "AllFighterDataCompiled/{}/script/animcmd/body".format(char)
                if trainingMode:
                    finalDir = "AllFighterDataCompiledTraining/{}/script/animcmd/body".format(char)
                os.makedirs(finalDir, exist_ok=True)
                os.rename("{}/effect.bin".format(compiledDir), "{}/effect.bin".format(finalDir))
            else:
                finalDir = "AllFighterDataCompiled/{}/script/animcmd/weapon/{}".format(char, bodyOrWeapon)
                if trainingMode:
                    finalDir = "AllFighterDataCompiledTraining/{}/script/animcmd/weapon/{}".format(char, bodyOrWeapon)
                os.makedirs(finalDir, exist_ok=True)
                os.rename("{}/effect.bin".format(compiledDir), "{}/effect.bin".format(finalDir))
            shutil.rmtree(compiledDir)

if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
    blklisted = False
    training = False
    if len(sys.argv) == 3:
        if sys.arv[2].find('t') != -1:
            training = True
        if sys.argv[2].find('b') != -1:
            blklisted = True
    currFile = ACMFile(sys.argv[1])
    print(currFile.processFile(isBlacklisted=blklisted, isTrainingOnly=training))
else:
    main()

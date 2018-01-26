import os, sys, struct, subprocess, shlex, glob, shutil
import disasm
if len(sys.argv) < 3:
    print("Usage: List of characters to be processed followed by replacement MSC folder")
    exit()
allChars = sys.argv[1:-1]
mscFolder = sys.argv[-1]

charsToFix = ["rockman", "szerosuit", "yoshi"]
aliasDict = {
    "toggleNumVar":0x1200004A,
    "hasEnteredVar":0x1200004B,
    "mashToggleVar":0x1200006E,
    "mashAttackVar":0x200023d,
    "isPlayerOneVar":0x200000B0,
    "playerOneDamageVar":0x2000230,
    "playerOneLockedDamageVar":0x200023c,
    "CPULockedDamageVar":0x2000236,
    "shouldLockP1DamageVar":0x2000239,
    "shouldLockCPUDamageVar":0x200023a,
    "lockConditionsSetVar":0x200023b,
    "hasSetDamageVar":0x200000B7,
    "zInputVar":0x200000B2,
    "xInputVar":0x200000B3,
    "aInputVar":0x200000B4,
    "bInputVar":0x200000B5,
    "rInputVar":0x200000B6,
    "stickXInputVar":0x11000012,
    "stickYInputVar":0x11000013,

    "canReallyAirdodgeVar":0x2000232,
    "canReallyAnyActionVar":0x2000233,

    "DIChangeVar":0x2000126,

    # up taunt toggles
    "fullMod":1,
    "hitboxVisOff":2,
    "inputDisplay":3,
    "vanilla":4,

    # down taunt toggles
    "mashAirdodge":0,
    "mashAttack":1,
    "mashJump":2,
    "randomGetup":3,
    "damage10":4,
    "damage1":5,
    "infiniteShield":6,
    "holdShield":7,
    "vanillaMash":8
}

if allChars == ["all"]:
    allChars = os.listdir("../../AllFighterData")
for dir in allChars:
    char = os.path.basename(dir)
    print("Disassembling {}...".format(char))
    os.makedirs("../../AllFighterMSCCompiled/{}/script/msc".format(char), exist_ok=True)
    devnull = open(os.devnull, 'w')
    subprocess.run(shlex.split("python3 disasm.py --char-std --123 --extension mscscript ../../AllFighterData/{}/script/msc/{}.mscsb output".format(char, char)), stdout=devnull)
    for scriptBasename in os.listdir(mscFolder):
        script = os.path.join(mscFolder, scriptBasename)
        if scriptBasename[:6] == "script":
            print("Replacing {}...".format(script))
        else:
            print("Adding {}...".format(script))
            with open("output/Scripts", "a") as scriptsFile:
                scriptsFile.write(scriptBasename+"\n")
        shutil.copyfile(script, "output/{}".format(scriptBasename))

    if char in charsToFix:
        print("Fixing {}...".format(char))
        fixFolder = "scriptFolders/{}Fix".format(char)
        for scriptBasename in os.listdir(fixFolder):
            script = os.path.join(fixFolder, scriptBasename)
            shutil.copyfile(script, "output/{}".format(scriptBasename))

    os.chdir("output")
    print("Reassembling {}...".format(char))
    with open("globals.txt", "a") as globalsFile:
        for varName in aliasDict:
            globalsFile.write(".alias 0x{:X},{}\n".format(aliasDict[varName],varName))

    subprocess.run(shlex.split("python3 ../asm.py --saveas test.mscsb"))
    print("Moving to AllFighterMSCCompiled...")
    os.rename("test.mscsb", "../../../AllFighterMSCCompiled/{}/script/msc/{}.mscsb".format(char, char))
    os.chdir("..")

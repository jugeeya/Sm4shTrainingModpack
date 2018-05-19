import os, sys, struct, subprocess, shlex, glob, shutil
import disasm
if len(sys.argv) < 3:
    print("Usage: List of characters to be processed followed by replacement MSC folder")
    exit()
allChars = sys.argv[1:-1]
mscFolder = sys.argv[-1]

charsToFix = ["rockman", "szerosuit", "yoshi", "shulk"]
aliasDict = {
    "toggleNumVar":0x1200004A,
    "hasEnteredVar":0x1200004B,
    "mashToggleVar":0x1200006E,
    "mashAttackVar":0x200023d,
    "spamOptionVar":0x2000240,
    "techOptionVar":0x2000241,
    # SaveState
    "P1SavedX":0x2000242,
    "P1SavedY":0x2000243,
    "P1SavedZ":0x2000244,
    "P1SavedLR":0x2000245,
    "P1SavedGroundAirState":0x12000246,
    "P1SavedPercent":0x2000247,
    "P1SavedState":0x12000248,
    "CPUSavedX":0x2000249,
    "CPUSavedY":0x200024a,
    "CPUSavedZ":0x200024b,
    "CPUSavedLR":0x200024c,
    "CPUSavedGroundAirState":0x1200024d,
    "CPUSavedPercent":0x200024e,
    "CPUSavedState":0x1200024f,
    # Lock Percent
    "isPlayerOneVar":0x200000B0,
    "playerOneDamageVar":0x2000230,
    "playerOneLockedDamageVar":0x200023c,
    "CPULockedDamageVar":0x2000236,
    "shouldLockP1DamageVar":0x2000239,
    "shouldLockCPUDamageVar":0x200023a,
    "lockConditionsSetVar":0x200023b,
    "hasSetDamageVar":0x200000B7,
    # InputDisplay
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
    "spamOption":3,
    "randomTech":4,
    "randomGetup":5,
    "damage10":6,
    "damage1":7,
    "infiniteShield":8,
    "holdShield":9,
    "vanillaMash":10
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

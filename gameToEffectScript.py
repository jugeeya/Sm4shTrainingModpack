import os.path
import struct
import sys
from collections import OrderedDict

# KuroganeHammer data
gameChars = "bayonetta,captain,cloud,dedede,diddy,donkey,duckhunt,falco,fox,gamewatch,ganon,gekkouga,ike,kamui,kirby,koopa,koopajr,link,littlemac,lizardon,lucario,lucas,lucina,luigi,mario,mariod,marth,metaknight,mewtwo,murabito,ness,pacman,palutena,peach,pikachu,pikmin,pit,pitb,purin,reflet,robot,rockman,rosetta,roy,ryu,samus,sheik,shulk,sonic,szerosuit,toonlink,wario,wiifit,yoshi,zelda".split(
    ",")
kuroChars = "Bayonetta,Captain%20Falcon,Cloud,King%20Dedede,Diddy%20Kong,Donkey%20Kong,Duck%20Hunt,Falco,Fox,Game%20And%20Watch,Ganondorf,Greninja,Ike,Corrin,Kirby,Bowser,Bowser%20Jr,Link,Little%20Mac,Charizard,Lucario,Lucas,Lucina,Luigi,Mario,Dr.%20Mario,Marth,Meta%20Knight,Mewtwo,Villager,Ness,PAC-MAN,Palutena,Peach,Pikachu,Olimar,Pit,Dark%20Pit,Jigglypuff,Robin,R.O.B,Mega%20Man,Rosalina%20And%20Luma,Roy,Ryu,Samus,Sheik,Shulk,Sonic,Zero%20Suit%20Samus,Toon%20Link,Wario,Wii%20Fit%20Trainer,Yoshi,Zelda".split(
    ",")

counterChars = "gekkouga,ike,kamui,littlemac,lucario,lucina,marth,palutena,peach,roy,shulk".split(",")

kuroMoves = "Jab 1,Medium Jab 1,Jab 2,Jab 3,Dash Attack,Ftilt,Ftilt,Ftilt,Light Ftilt,Medium Ftilt,Ftilt 2,Ftilt 3,Utilt,Light Utilt,Medium Utilt,Dtilt,Light Dtilt,Medium Dtilt,Fsmash,Usmash,Dsmash,Standing Grab,Dash Grab,Pivot Grab,Nair,Fair,Fair 2,Fair 3,Bair,Uair,Dair".split(",")
gameMoves = "Attack11,Attack11s,Attack12,Attack13,AttackDash,AttackS3,AttackS3Hi,AttackS3Lw,0x008C1CDD,0x07E1D8C4,0x063AA9C2,0x713D9954,AttackHi3,AttackHi3w,AttackHi3s,AttackLw3,AttackLw3w,AttackLw3s,AttackS4,AttackHi4,AttackLw4,Catch,CatchDash,CatchTurn,AttackAirN,AttackAirF,AttackAirF2,AttackAirF3,AttackAirB,AttackAirHi,AttackAirLw".split(",")

gameMovesToKuro = {}
for i in range(len(gameMoves)):
    gameMovesToKuro[gameMoves[i]] = kuroMoves[i]

# game code lines
asynchronousTimer = "Asynchronous_Timer(Frames={})"
synchronousTimer = "Synchronous_Timer(Frames={})"
setBoneIntangability = "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)"
normalOrSpecialHitbox = "Graphic_Effect6(Graphic=0x1000013, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
extendedHitbox = "Graphic_Effect6(Graphic=0x1000013, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
normalOrSpecialHitboxNew = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown={}, unknown={}, unknown={})"
extendedHitboxNew = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown={}, unknown={}, unknown={})"
grabHitbox = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown=0x0, unknown=0x437F0000, unknown=0x0)"
terminateGraphic13 = "Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)"
terminateGraphic31 = "Terminate_Graphic_Effect(Graphic=0x1000031, unknown=0x1, unknown=0x1)"
colorOverlay = "Color_Overlay(Red={}, Green={}, Blue={}, Alpha={})"
terminateOverlays = "Terminate_Overlays()"
subroutine = "Subroutine(Hash={})"
extsubroutine = "External_Subroutine(Hash={})"
downEffect1 = "Graphic_Effect2(Graphic=0x1000008, Bone=0x0, Z=0, Y=0, X=0, ZRot=0, YRot=0, XRot=0, Size=1, RandomZ=0, RandomY=0, RandomX=0, RandomZRot=0, RandomYRot=0, RandomXRot=0, Terminate=0x0)"
downEffect2 = "DOWN_EFFECT(unknown=0x100000A, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0)"
setLoop = "Set_Loop(Iterations={}){{"
ifCompare = "If_Compare(Variable={}, Method={}, Variable2={})"
ifCompare2 = "If_Compare2(Variable={}, Method={}, Value={})"
ifBitIsSet = "If_Bit_is_Set(Variable={})"
isExistArticle = "IS_EXIST_ARTICLE(Unknown={})"
someCompare = "unk_477705C2(unknown={}, unknown={}, unknown={})"
someCompare2 = "unk_2DA7E2B6(unknown={}, unknown={}, unknown={})"
TRUEComp = "TRUE(Unknown={}){{"
FALSEComp = "FALSE(Unknown={}){{"
bitVariableSet = "Bit_Variable_Set(Variable={})"
bitVariableClear = "Bit_Variable_Clear(Variable={})"
goto = "Goto(Unknown={})"
endLoopOrCompare = "}"
scriptEnd = "Script_End()"
testHitbox = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown={}, unknown={}, unknown={}, unknown={})"
testTerminate = "Terminate_Graphic_Effect(Graphic={}, unknown={}, unknown={})"

effectLines = "\tEffect()\n\t{\r\n"

# effectStringDict functions as follows:
# effectString: [hitboxID, isDeleted, hitboxOrGrabbox]
#                ID,        [-1,0,1]    [-1,0,1]
effectStringDict = OrderedDict()

falseVals = []
falseIndex = 0
trueVals = []
trueIndex = 0
RED = ['255', '0', '0', '128']
GREEN = ['0', '255', '0', '128']
BLUE = ['0', '0', '255', '128']
ORANGE = ['255', '165', '0', '128']
MAGENTA = ['255', '0', '255', '128']

blacklisted = False
inLoop = False
inCompare = 0
FAF = 100000
currentFrame = 0

def moreHitboxesExist(remainingLines):
    for i in remainingLines:
        if i.find("Hitbox") != -1 or i.find("Grab") != -1:
            return True
    return False

def getTSVLine(moveName, tsvLines):
    for line in tsvLines:
        for value in line.split("\t"):
            if value[:len(moveName)] == moveName:
                return line
    return "Not Found"

def didProcessEndlag(lines, index, basename, tsvLines):
    global effectLines, FAF
    if not moreHitboxesExist(lines[index + 1:]):
        currMove = basename[:-4]
        if currMove in gameMoves and len(tsvLines) >= 1:
            kuroMove = gameMovesToKuro[currMove]
            testMultiHitb2 = kuroMove + " 2"
            testMultiHitb3 = kuroMove + " 3"
            if kuroMove[-1] == "1":
                testMultiHitb2 = kuroMove[:-1] + "2"
                testMultiHitb3 = kuroMove[:-1] + "3"
            if kuroMove[-1] == "2":
                testMultiHitb3 = kuroMove[:-1] + "3"
            if getTSVLine(testMultiHitb2, tsvLines) == "Not Found" and getTSVLine(testMultiHitb3, tsvLines) == "Not Found":
                addEffect(asynchronousTimer.format(currentFrame))
                addEffect(colorOverlay.format(*GREEN))
                currTSVLine = getTSVLine(gameMovesToKuro[currMove], tsvLines)
                FAFStr = currTSVLine.split('\t')[-1]
                FAFStr = FAFStr.split(' ')[0]
                FAF = int(FAFStr)
                addEffect(asynchronousTimer.format(FAF))
                addEffect(terminateOverlays)
                if not inLoop and not inCompare:
                    addEffect(scriptEnd)
                if blacklisted:
                    effectLines = "\t\t" + asynchronousTimer.format(currentFrame) + "\r\n"
                    effectLines = effectLines + "\t\t" + colorOverlay.format(*GREEN) + "\r\n"
                    effectLines = effectLines + "\t\t" + asynchronousTimer.format(FAF) + "\r\n"
                    effectLines = effectLines + "\t\t" + terminateOverlays + "\r\n"
                    effectLines = effectLines + "\t\t" + scriptEnd + "\r\n"
                return True
    if blacklisted:
        effectLines = "\t\t" + scriptEnd + "\r\n"
    return False

def editLastTrue(value):
    global effectLines, trueIndex
    if value == 2:
        removeLastEffectString()
        removeLastEffectString()
        removeLastEffectString()
        trueIndex = trueIndex - 1
    else:
        i = effectLines.rfind("TRUE")
        trueOnwards = effectLines[i:]
        effectLines = effectLines[:i] + TRUEComp.format(hex(value)) + effectLines[i + trueOnwards.find(")")+2:]

def falseExists():
    for e in effectStringDict:
        if e[:len("FALSE")] == "FALSE":
            return True
    return False

def parseUntilLastTrue(trueNum):
    trueVals[trueNum] = 0
    allEffectLines = effectLines.split("\r\n")[:-1]
    indices = []
    for i in range(len(allEffectLines)):
        allEffectLines[i] = removeBeginningWhitespace(allEffectLines[i])
        if allEffectLines[i][:len("TRUE")] == "TRUE":
            indices.append(i)
    for q in range(indices[trueNum],len(allEffectLines)-1):
        thisParamList = getParamList(allEffectLines[q])
        if thisParamList[0] != "":
            trueVals[trueNum] = trueVals[trueNum] + len(thisParamList) + 1
        else:
            trueVals[trueNum] = trueVals[trueNum] + len(thisParamList)
    if falseExists():
        trueVals[trueNum] = trueVals[trueNum] + 2

def editLastFalse(value):
    global effectLines
    i = effectLines.rfind("FALSE")
    falseOnwards = effectLines[i:]
    effectLines = effectLines[:i] + FALSEComp.format(hex(value)) + effectLines[i + falseOnwards.find(")")+2:]

def parseUntilLastFalse(falseNum):
    falseVals[falseNum] = 0
    allEffectLines = effectLines.split("\r\n")[:-1]
    indices = []
    for i in range(len(allEffectLines)):
        allEffectLines[i] = removeBeginningWhitespace(allEffectLines[i])
        if allEffectLines[i][:len("FALSE")] == "FALSE":
            indices.append(i)
    for q in range(indices[falseNum],len(allEffectLines)-1):
        thisParamList = getParamList(allEffectLines[q])
        if thisParamList[0] != "":
            falseVals[falseNum] = falseVals[falseNum] + len(thisParamList) + 1
        else:
            falseVals[falseNum] = falseVals[falseNum] + len(thisParamList)
        # print(allEffectLines[q], len(thisParamList), falseVals[falseNum])

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def getHexFloat(value):
    hexFloat = str(float_to_hex(value)).upper()
    return "".join(c.lower() if (c == "X") else c for i, c in enumerate(hexFloat))

def getParamList(line):
    parameters = line[line.find("(") + 1:line.find(")")]
    fullParamList = parameters.split(',')
    paramList = [x[x.find("=") + 1:] for x in fullParamList]
    return paramList

def addEffect(effectString):
    addEffectID(effectString, -1, -1)

def markDeleted(hitboxID, hitboxOrGrabbox):
    numReadded = 0
    for e in effectStringDict:
        currlist = effectStringDict[e]
        if currlist[1] == 0 and currlist[2] == hitboxOrGrabbox:
            if currlist[0] != hitboxID:
                # addEffectID(e, currlist[0], currlist[2])
                addEffect(e)
                numReadded = numReadded + 1
    i = 0
    for e in effectStringDict: # mark all except just added ones
        if i == len(effectStringDict) - numReadded - 1:
            break
        currlist = effectStringDict[e]
        if currlist[1] == 0 and currlist[2] == hitboxOrGrabbox:
            if currlist[0] == hitboxID:
                currlist[1] = 1
        i = i + 1

def markAllDeleted(hitboxOrGrabbox):
    for e in effectStringDict:
        currlist = effectStringDict[e]
        if currlist[2] == hitboxOrGrabbox:
            effectStringDict[e][1] = 1

def addEffectID(effectString, hitboxID, hitboxOrGrabbox):
    global effectLines, effectStringDict
    if hitboxID != -1:
        for e in effectStringDict:
            currlist = effectStringDict[e]
            if hitboxID == currlist[0] and currlist[1] == 0 and currlist[2] == hitboxOrGrabbox:  # equal ID, not deleted, hitbox/grabbox
                addEffect(terminateGraphic13)
                markAllDeleted(hitboxOrGrabbox)
                break
    if not blacklisted:
        effectLines = effectLines + "\t\t"
    tabs = inCompare
    if inLoop:
       tabs = tabs + 1
    for q in range(tabs):
        if not blacklisted:
            effectLines = effectLines + "    "

    if not blacklisted:
        effectLines = effectLines + effectString + "\r\n"
    effectStringDict[effectString] = [hitboxID, 0, hitboxOrGrabbox]

def getLastEffectString():
    allEffectLines = effectLines.split("\r\n")
    return removeBeginningWhitespace(allEffectLines[-2:-1])[0]

def removeBeginningWhitespace(string):
    removed = ""
    for q in range(len(string)):
        if not string[q].isspace():
            removed = string[q:]
            break
    return removed

def removeLastEffectString():
    global effectLines
    tabIndex = effectLines.rfind("\t")
    while (effectLines[tabIndex] == "\t"):
        tabIndex = tabIndex - 1
    effectLines = effectLines[:tabIndex+1]

def removeLastEffect(effectString):
    global effectLines
    currstr = "\t\t" + effectString + "\r\n"
    effectLines = effectLines[:-len(currstr)]

def printOutput(lines):
    inEffect = False
    for i in lines:
        if i == "\tEffect()\n\t{\r":
            inEffect = True
            print(effectLines, end="\t}\n\r\n")
        if not inEffect:
            if i != "\t\tTRUE(Unknown=0x2)\r":
                print(i, end="\n")
        else:
            if i == "\t}\n\r":
                inEffect = False

def printBlacklistedOutput(lines):
    inEffect = False
    global effectLines
    if effectLines == "\tEffect()\n\t{\r\n":
        effectLines = effectLines + "\t}\n\r\n"
    for i in lines:
        if i == "\tEffect()\n\t{\r":
            inEffect = True
            # print(effectLines, end="\t}\n\r\n")
        if not inEffect:
            if i != "\t\tTRUE(Unknown=0x2)\r":
                print(i, end="\n")
        else:
            if i == "\t\tScript_End()\r":
                print(effectLines, end="")
                inEffect = False
            elif i == "\t}\n\r":
                print(i)
                inEffect = False
            else:
                print(i, end="\n")

def getDamageRGB(damageStr, angleStr):
    damage = float(damageStr)
    angle = int(angleStr, 16)
    if 240 <= angle <= 300:
        red = getHexFloat(255)
        green = getHexFloat(0)
        blue = getHexFloat(230)
    elif damage == 0:
        red = getHexFloat(255)
        green = getHexFloat(255)
        blue = getHexFloat(255)
    elif damage > 15:
        red = getHexFloat(255)
        green = getHexFloat(0)
        blue = getHexFloat(0)
    else:
        red = getHexFloat(255)
        green = getHexFloat(230 - (damage * 230 / 15))
        blue = getHexFloat(0)

    return red, green, blue

def addDodgeEffects2(dodgeActive):
    addEffect(asynchronousTimer.format(dodgeActive[0]))
    addEffect(colorOverlay.format(*BLUE))
    addEffect(asynchronousTimer.format(str(int(dodgeActive[1]) + 1)))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def addDodgeEffects(dodgeActive, dodgeFAF):
    # starting frames
    addEffect(colorOverlay.format(*GREEN))
    # invuln
    addEffect(asynchronousTimer.format(dodgeActive[0]))
    addEffect(terminateOverlays)
    addEffect(colorOverlay.format(*BLUE))
    addEffect(asynchronousTimer.format(str(int(dodgeActive[1]) + 1)))
    addEffect(terminateOverlays)
    # lag
    addEffect(colorOverlay.format(*GREEN))
    addEffect(asynchronousTimer.format(dodgeFAF))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def addLagEffects(lagLength):
    addEffect(asynchronousTimer.format("1"))
    addEffect(colorOverlay.format(*GREEN))
    addEffect(asynchronousTimer.format(str(int(lagLength) + 1)))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def main():
    global effectLines, inLoop, inCompare, falseVals, trueVals, falseIndex, trueIndex, currentFrame, blacklisted
    if len(sys.argv) < 2:
        print("Needs one argument: .acm move file path, optional blacklisted second arg")
        exit()
    filename = sys.argv[1]
    if len(sys.argv) == 3:
        blacklistArg = sys.argv[2]
        if blacklistArg == 'y':
            blacklisted = True
            effectLines = ""

    with open(filename, newline="\r\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    inMain = False
    shouldExitLoop = False
    gotoNum = 0
    offsetBegin = 0
    offsetEnd = 0
    prevFrame = 0
    inFalse = 0
    inTrue = 0
    processedEndlag = False

    loopNum = 0
    loopLines = 0

    tsvLines = []

    # tsvData found in TSV folder; read any file for example layout
    charName = os.path.split(os.path.dirname(filename))[0][:-5]
    if charName[-4:] == "body":
        charName = charName[:-4]
        tsvPath = "TSV/{}.tsv".format(charName)
        if os.path.isfile(tsvPath):
            with open(tsvPath) as tsv:
                tsvLines = tsv.readlines()
            tsvLines = [x.strip('\n') for x in tsvLines]

    basename = os.path.basename(filename)

    spotdodge = "EscapeN.acm"
    froll = "EscapeF.acm"
    broll = "EscapeB.acm"
    airdodge = "EscapeAir.acm"
    shielding = "Guard.acm"
    shieldOn = "GuardOn.acm"
    unshield = "GuardOff.acm"
    shieldDamage = "GuardDamage.acm"
    ledgecatch = "CliffCatch.acm"
    groundedfootstoolPose = "StepPose.acm"
    groundedfootstoolBack = "0xE0D78C1E.acm"
    spinningAnim = "DamageFlyRoll.acm"
    ledgegetup = "CliffClimbQuick.acm"
    ledgeroll = "CliffEscapeQuick.acm"
    ledgejump = "CliffJumpQuick1.acm"
    ledgeattack = "CliffAttackQuick.acm"
    jumpsquat = "JumpSquat.acm"
    lightLanding = "LandingLight.acm"
    hardLanding = "LandingHeavy.acm"
    landingAirN = "LandingAirN.acm"
    landingAirF = "LandingAirF.acm"
    landingAirB = "LandingAirB.acm"
    landingAirHi = "LandingAirHi.acm"
    landingAirLw = "LandingAirLw.acm"
    passive = "Passive.acm"
    passiveF = "PassiveStandF.acm"
    passiveB = "PassiveStandB.acm"
    downStandU = "DownStandU.acm"
    downStandD = "DownStandD.acm"
    downForwardU = "DownForwardU.acm"
    downForwardD = "DownForwardD.acm"
    downBackU = "DownBackU.acm"
    downBackD = "DownBackD.acm"
    downBoundU = "DownBoundU.acm"
    downBoundD = "DownBoundD.acm"
    jabresetU = "DownDamageU3.acm"
    jabresetD = "DownDamageD3.acm"

    if didHandleEdgeCase(charName, basename):
        str = "This conditional is a placeholder."
    elif basename == unshield:
        addLagEffects('7')
    elif basename == shieldDamage:
        addEffect(colorOverlay.format(*GREEN))
        addEffect(scriptEnd)
    elif basename == ledgecatch:
        addLagEffects('2')
    elif basename == groundedfootstoolPose:
        addLagEffects('8')
    elif basename == groundedfootstoolBack:
        addLagEffects('20')
    elif basename == spinningAnim:
        addEffect(asynchronousTimer.format('1'))
        addEffect(colorOverlay.format(*ORANGE))
        addEffect(scriptEnd)
    elif basename == spotdodge:
        addDodgeEffects(tsvLines[0].split("\t")[0:2], tsvLines[1].split("\t")[0])
    elif basename == froll:
        addDodgeEffects(tsvLines[2].split("\t")[0:2], tsvLines[3].split("\t")[0])
    elif basename == broll:
        addDodgeEffects(tsvLines[4].split("\t")[0:2], tsvLines[5].split("\t")[0])
    elif basename == airdodge:
        addDodgeEffects(tsvLines[6].split("\t")[0:2], tsvLines[7].split("\t")[0])
    elif basename == ledgejump:
        addDodgeEffects2(tsvLines[8].split("\t")[0:2])
    elif basename == ledgeroll:
        addDodgeEffects(tsvLines[10].split("\t")[0:2], tsvLines[11].split("\t")[0])
    elif basename == ledgegetup:
        addDodgeEffects(tsvLines[12].split("\t")[0:2], tsvLines[13].split("\t")[0])
    elif basename == jumpsquat:
        addLagEffects(tsvLines[16].split("\t")[0])
    elif basename == lightLanding:
        addLagEffects(tsvLines[17].split("\t")[0])
    elif basename == hardLanding:
        addLagEffects(tsvLines[18].split("\t")[0])
    elif basename == landingAirN:
        addLagEffects(tsvLines[19].split("\t")[0])
    elif basename == landingAirF:
        addLagEffects(tsvLines[20].split("\t")[0])
    elif basename == landingAirB and charName != "pikachu":
        addLagEffects(tsvLines[21].split("\t")[0])
    elif basename == landingAirHi:
        addLagEffects(tsvLines[22].split("\t")[0])
    elif basename == landingAirLw and charName != "pikachu":
        addLagEffects(tsvLines[23].split("\t")[0])
    elif basename == downStandU:
        addDodgeEffects(tsvLines[25].split("\t")[0:2], tsvLines[26].split("\t")[0])
    elif basename == downStandD:
        addDodgeEffects(tsvLines[27].split("\t")[0:2], tsvLines[28].split("\t")[0])
    elif basename == downForwardU:
        addDodgeEffects(tsvLines[29].split("\t")[0:2], tsvLines[30].split("\t")[0])
    elif basename == downForwardD:
        addDodgeEffects(tsvLines[31].split("\t")[0:2], tsvLines[32].split("\t")[0])
    elif basename == downBackU:
        addDodgeEffects(tsvLines[33].split("\t")[0:2], tsvLines[34].split("\t")[0])
    elif basename == downBackD:
        addDodgeEffects(tsvLines[35].split("\t")[0:2], tsvLines[36].split("\t")[0])
    elif basename == passive:
        addDodgeEffects(tsvLines[37].split("\t")[0:2], tsvLines[38].split("\t")[0])
    elif basename == passiveF:
        addDodgeEffects(tsvLines[39].split("\t")[0:2], tsvLines[40].split("\t")[0])
    elif basename == passiveB:
        addDodgeEffects(tsvLines[41].split("\t")[0:2], tsvLines[42].split("\t")[0])
    elif basename == downBoundU:
        addEffect(downEffect1)
        addEffect(downEffect2)
        addLagEffects(tsvLines[43].split("\t")[1])
    elif basename == downBoundD:
        addEffect(downEffect1)
        addEffect(downEffect2)
        addLagEffects(tsvLines[44].split("\t")[1])
    elif basename in {jabresetU, jabresetD}:
        addEffect(asynchronousTimer.format("1"))
        addEffect(colorOverlay.format(*GREEN))
        addEffect(scriptEnd)
    else:
        if basename == ledgeattack:
            addDodgeEffects2(tsvLines[14].split("\t")[0:2])
            removeLastEffect(scriptEnd)
        index = 0
        while index < len(lines):
            iorig = lines[index]
            i = removeBeginningWhitespace(iorig)

            # print(i, index)

            if i == "Main()\n\t{\r":
                inMain = True
                if lines[index + 1] == "\t}\n\r":
                    break
            if shouldExitLoop:
                break
            if inMain:
                paramList = getParamList(i)

                endlooporcompare = "}"
                if i[:len(endlooporcompare)] == endlooporcompare:
                    if inCompare:
                        inCompare = inCompare - 1
                        addEffect(endLoopOrCompare)
                    if inLoop:
                        inLoop = False
                        addEffect(endLoopOrCompare)
                    if inFalse:
                        parseUntilLastFalse(falseIndex - 1)
                        editLastFalse(falseVals[falseIndex-1])
                        inFalse = inFalse - 1
                        # falseIndex = falseIndex - 1
                    if inTrue:
                        parseUntilLastTrue(trueIndex - 1)
                        editLastTrue(trueVals[trueIndex-1])
                        inTrue = inTrue - 1
                        # trueIndex = trueIndex - 1

                compare = "If_Compare"
                compare2 = "If_Compare2"
                if i[:len(compare2)] == compare2:
                    addEffect(ifCompare2.format(paramList[0], paramList[1], paramList[2]))
                elif i[:len(compare)] == compare:
                    addEffect(ifCompare.format(paramList[0], paramList[1], paramList[2]))
                ifBitIsSetStr = "If_Bit_is_Set"
                if i[:len(ifBitIsSetStr)] == ifBitIsSetStr:
                    addEffect(ifBitIsSet.format(paramList[0]))
                isExistArticleStr = "IS_EXIST_ARTICLE"
                if i[:len(isExistArticleStr)] == isExistArticleStr:
                    addEffect(isExistArticle.format(paramList[0]))
                someCompareStr = "unk_477705C2"
                if i[:len(someCompareStr)] == someCompareStr:
                    addEffect(someCompare.format(paramList[0], paramList[1], paramList[2]))
                someCompareStr2 = "unk_2DA7E2B6"
                if i[:len(someCompareStr2)] == someCompareStr2:
                    addEffect(someCompare2.format(paramList[0], paramList[1], paramList[2]))

                TRUEstr = "TRUE"
                if i[:len(TRUEstr)] == TRUEstr:
                    addEffect(TRUEComp.format(paramList[0]))
                    inCompare = inCompare + 1
                    trueIndex = trueIndex + 1
                    inTrue = inTrue + 1
                    trueVals.append(0)

                FALSEstr = "FALSE"
                if i[:len(FALSEstr)] == FALSEstr:
                    addEffect(FALSEComp.format(paramList[0]))
                    inCompare = inCompare + 1
                    falseIndex = falseIndex + 1
                    inFalse = inFalse + 1
                    falseVals.append(0)

                gotoStr = "Goto"
                if i[:len(gotoStr)] == gotoStr:
                    addEffect(goto.format(-gotoNum))
                    gotoNum = 0

                loop = "Set_Loop"
                if i[:len(loop)] == loop:
                    loopNum = int(paramList[0]) if paramList[0] != "-1" else 0
                    addEffect(setLoop.format(loopNum))
                    inLoop = True
                elif inLoop:
                    loopLines = loopLines + 1

                looprest = "Loop_Rest()"
                if i[:len(looprest)] == looprest:
                    addEffect(looprest)

                armor = "Set_Armor"
                if i[:len(armor)] == armor:
                    state = paramList[0]
                    if state == "0x0":
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(*MAGENTA))

                bodycoll = "Body_Collision"
                if i[:len(bodycoll)] == bodycoll:
                    state = paramList[0]
                    if state == "0x0":
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(*BLUE))

                detect = "Search_Collision"
                if i[:len(detect)] == detect:
                    bone = paramList[2]
                    size = getHexFloat(float(paramList[3]) * 19 / 200)
                    z = getHexFloat(float(paramList[4]))
                    y = getHexFloat(float(paramList[5]))
                    x = getHexFloat(float(paramList[6]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255)
                    addEffectID(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue), paramList[0], 1)

                subr = "Subroutine"
                if i[:len(subr)] == subr:
                    hashNum = paramList[0]
                    addEffect(subroutine.format(hashNum))

                extsubr = "External_Subroutine"
                if i[:len(extsubr)] == extsubr:
                    hashNum = paramList[0]
                    addEffect(extsubroutine.format(hashNum))

                waitloopclr = "WAIT_LOOP_CLR()"
                if i[:len(waitloopclr)] == waitloopclr:
                    addEffect(waitloopclr)

                defensive = "Defensive_Collision"
                if i[:len(defensive)] == defensive:
                    addEffect(colorOverlay.format(*RED))

                bitvarset = "Bit_Variable_Set"
                if i[:len(bitvarset)] == bitvarset:
                    var = paramList[0]
                    specialLw = "SpecialLw"
                    if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                        addEffect(colorOverlay.format(*RED))

                bitvarclear = "Bit_Variable_Clear"
                if i[:len(bitvarclear)] == bitvarclear:
                    var = paramList[0]
                    if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                        addEffect(terminateOverlays)

                terminateDefensive = "Terminate_Defensive_Collision"
                if i[:len(terminateDefensive)] == terminateDefensive:
                    addEffect(terminateOverlays)

                basicvarset = "Basic_Variable_Set"
                if i[:len(basicvarset)] == basicvarset:
                    if offsetBegin == 0 and paramList[1] == "0x1100000F":
                        offsetBegin = int(paramList[0], 16)
                        prevFrame = int(getParamList(getLastEffectString())[0])
                        removeLastEffect(asynchronousTimer.format(prevFrame))
                        addEffect(asynchronousTimer.format(prevFrame + offsetBegin))
                    elif paramList[1] == "0x11000010":
                        offsetEnd = int(paramList[0], 16)

                asyncTimer = "Asynchronous_Timer"
                if i[:len(asyncTimer)] == asyncTimer and not processedEndlag:
                    if offsetEnd != 0:
                        addEffect(asynchronousTimer.format(offsetEnd + prevFrame))
                        addEffect(terminateGraphic13)
                        addEffect(asynchronousTimer.format(offsetBegin + int(paramList[0])))
                        prevFrame = int(paramList[0])
                    else:
                        addEffect(asynchronousTimer.format(paramList[0]))
                    currentFrame = int(paramList[0])

                syncTimer = "Synchronous_Timer"
                if i[:len(syncTimer)] == syncTimer and not processedEndlag:
                    addEffect(synchronousTimer.format(paramList[0]))
                    currentFrame = currentFrame + int(paramList[0])

                undoBone = "Undo_Bone_Collision"
                if i[:len(undoBone)] == undoBone:
                    addEffect(terminateGraphic31)

                removeHitb = "Remove_All_Hitboxes"
                enableAction = "Enable Action Status"
                if i[:len(removeHitb)] == removeHitb or i[:len(enableAction)] == enableAction:
                    addEffect(terminateGraphic13)
                    markAllDeleted(0)
                    if didProcessEndlag(lines, index, basename, tsvLines):
                        if not inLoop and not inCompare:
                            break
                        processedEndlag = True

                terminateGrab = "Terminate_Grab_Collisions"
                if i[:len(terminateGrab)] == terminateGrab:
                    addEffect(terminateGraphic13)
                    markAllDeleted(1)
                    if didProcessEndlag(lines, index, basename, tsvLines):
                        if not inLoop and not inCompare:
                            break
                        processedEndlag = True

                deleteGrab = "Delete_Catch_Collision"
                if i[:len(deleteGrab)] == deleteGrab:
                    addEffect(terminateGraphic13)
                    markDeleted(paramList[0], 1)
                    if didProcessEndlag(lines, index, basename, tsvLines):
                        if not inLoop and not inCompare:
                            break
                        processedEndlag = True

                deleteHitb = "Delete_Hitbox"
                if i[:len(deleteHitb)] == deleteHitb:
                    addEffect(terminateGraphic13)
                    markDeleted(paramList[0], 0)
                    if didProcessEndlag(lines, index, basename, tsvLines):
                        if not inLoop and not inCompare:
                            break
                        processedEndlag = True

                boneIntangability = "Set_Bone_Intangability"
                if i[:len(boneIntangability)] == boneIntangability:
                    bone = paramList[0]
                    addEffect(setBoneIntangability.format(bone))

                if not blacklisted:
                    hitb = "Hitbox"
                    specialHitb = "Special_Hitbox"
                    collateralHitb = "Collateral_Hitbox"
                    if i[:len(hitb)] == hitb or i[:len(specialHitb)] == specialHitb or i[:len(collateralHitb)] == collateralHitb:
                        bone = paramList[2]
                        size = getHexFloat(float(paramList[8]) * 19 / 200)
                        z = getHexFloat(float(paramList[9]))
                        y = getHexFloat(float(paramList[10]))
                        x = getHexFloat(float(paramList[11]))
                        red, green, blue = getDamageRGB(paramList[3], paramList[4])
                        # addEffect(normalOrSpecialHitbox.format(bone, z, y, x, size))
                        addEffectID(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue), paramList[0], 0)

                    extendedHitb = "Extended_Hitbox"
                    if i[:len(extendedHitb)] == extendedHitb:
                        bone = paramList[2]
                        size = getHexFloat(float(paramList[8]) * 19 / 200)
                        zinit = float(paramList[9])
                        yinit = float(paramList[10])
                        xinit = float(paramList[11])
                        zfinal = float(paramList[24])
                        yfinal = float(paramList[25])
                        xfinal = float(paramList[26])
                        for j in range(0, 4):
                            zcurr = getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
                            ycurr = getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
                            xcurr = getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
                            red, green, blue = getDamageRGB(paramList[3], paramList[4])
                            # addEffect(extendedHitbox.format(bone, zcurr, ycurr, xcurr, size))
                            if j == 0:
                                addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), paramList[0], 0)
                            else:
                                addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), -1, 0)

                    extendedSpecialHitb = "Extended_Special_Hitbox"
                    if i[:len(extendedSpecialHitb)] == extendedSpecialHitb:
                        bone = paramList[2]
                        size = getHexFloat(float(paramList[8]) * 19 / 200)
                        zinit = float(paramList[9])
                        yinit = float(paramList[10])
                        xinit = float(paramList[11])
                        zfinal = float(paramList[40])
                        yfinal = float(paramList[41])
                        xfinal = float(paramList[42])
                        for j in range(0, 8):
                            zcurr = getHexFloat(zinit + ((zfinal - zinit) / 7 * j))
                            ycurr = getHexFloat(yinit + ((yfinal - yinit) / 7 * j))
                            xcurr = getHexFloat(xinit + ((xfinal - xinit) / 7 * j))
                            red, green, blue = getDamageRGB(paramList[3], paramList[4])
                            # addEffect(extendedHitbox.format(bone, zcurr, ycurr, xcurr, size))
                            if j == 0:
                                addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), paramList[0], 0)
                            else:
                                addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), -1, 0)

                grabcoll2 = "Grab_Collision2"
                grabcoll = "Grab_Collision"
                if i[:len(grabcoll2)] == grabcoll2:
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255)
                    # addEffectID(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue), paramList[0], 1)
                    addEffectID(grabHitbox.format(bone, z, y, x, size), paramList[0], 1)
                elif i[:len(grabcoll)] == grabcoll:
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    addEffectID(grabHitbox.format(bone, z, y, x, size), paramList[0], 1)

                grabHitb = "Extended_Grab_Collision"
                if i[:len(grabHitb)] == grabHitb:
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    zinit = float(paramList[3])
                    yinit = float(paramList[4])
                    xinit = float(paramList[5])
                    zfinal = zinit  # float(paramList[8]) #zinit??
                    yfinal = float(paramList[9])
                    xfinal = float(paramList[10])
                    for j in range(0, 3):
                        zcurr = getHexFloat(zinit + ((zfinal - zinit) / 2 * j))
                        ycurr = getHexFloat(yinit + ((yfinal - yinit) / 2 * j))
                        xcurr = getHexFloat(xinit + ((xfinal - xinit) / 2 * j))
                        if j == 0:
                            addEffectID(grabHitbox.format(bone, zcurr, ycurr, xcurr, size), paramList[0], 1)
                        else:
                            addEffectID(grabHitbox.format(bone, zcurr, ycurr, xcurr, size), -1, 1)

                if inLoop and i[:len(loop)] != loop:
                    thisParamList = getParamList(getLastEffectString())
                    if thisParamList[0] != "":
                        gotoNum = gotoNum + len(thisParamList) + 1
                    else:
                        gotoNum = gotoNum + len(thisParamList)

                scriptFin = "Script_End()"
                if i[:len(scriptFin)] == scriptFin:
                    if offsetBegin != 0:
                        addEffect(asynchronousTimer.format(prevFrame + offsetEnd))
                        addEffect(terminateGraphic13)
                    addEffect(scriptEnd)
                    inMain = False
                    shouldExitLoop = True
            index = index + 1

    if blacklisted:
        printBlacklistedOutput(lines)
    else:
        printOutput(lines)

def didHandleEdgeCase(char, move):
    global inLoop, inCompare
    if char == "cloud":
        if move == "0xF37FC0B3.acm":  # SpecialHiFall
            addEffect(asynchronousTimer.format('1'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x40000000', '0x41000000', '0x3E428F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x40000000', '0x40D55555', '0x3E428F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x40000000', '0x40AAAAAB', '0x3E428F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x40000000', '0x40800000', '0x3E428F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x40933333', '0x41100000', '0x3EC28F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x408EEEEF', '0x40D55555', '0x3EC28F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x408AAAAB', '0x408AAAAB', '0x3EC28F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(extendedHitboxNew.format('0x0', '0x0', '0x40866666', '0x40000000', '0x3EC28F5C', '0x437E0000', '0x0', '0x437E0000'))
            addEffect(scriptEnd)
            return True
        if move == "0xFB284F7A.acm":
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40A6DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40ADB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40B49249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40BB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40C24925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40C92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40D00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41700000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x415C9249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41492492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x4135B6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41224925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x410EDB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40F6DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40D00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=8)")
            addEffect("Asynchronous_Timer(Frames=9)")
            addEffect("Asynchronous_Timer(Frames=10)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41680000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41549249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41412492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x412DB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x411A4925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x4106DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40E6DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=11)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41680000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41549249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41412492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x412DB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x411A4925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x4106DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40E6DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41680000, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41549249, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x41412492, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x412DB6DB, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x411A4925, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x4106DB6E, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40E6DB6E, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x19, unknown=0x0, unknown=0x40C00000, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(asynchronousTimer.format('12'))
            addEffect(terminateOverlays)
            addEffect("Asynchronous_Timer(Frames=14)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=15)")
            addEffect("Asynchronous_Timer(Frames=25)")
            addEffect("Asynchronous_Timer(Frames=29)")
            addEffect("Asynchronous_Timer(Frames=35)")
            addEffect("Asynchronous_Timer(Frames=36)")
            addEffect("Asynchronous_Timer(Frames=40)")
            addEffect("Script_End()")
            return True
    if char == "kamui":
        if move in {"AttackS4.acm", "AttackS4Hi.acm", "AttackS4Lw.acm"}:
            addEffect(scriptEnd)
            return True
        if move == "SpecialSJump.acm":
            addDodgeEffects2(['2', '5'])
            return True
        if move == "SpecialLw.acm":
            addEffect(asynchronousTimer.format('6'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect(asynchronousTimer.format('7'))
            addEffect(terminateOverlays)
            addEffect(colorOverlay.format('255', '0', '0', '128'))
            addEffect(asynchronousTimer.format('25'))
            addEffect(terminateOverlays)
            addEffect(scriptEnd)
            return True
        if move == "SpecialLwHit.acm":
            addDodgeEffects2(['1','49'])
            return True
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=3)")
            addEffect("Synchronous_Timer(Frames=7)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(synchronousTimer.format('8'))
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0xBF800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x3F36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x3FA49249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x3FEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x401B6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0xC1600000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0xC11C9249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0xC0B24925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0xBFADB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0x4036DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0x40E24925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0x41349249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40600000, unknown=0x41780000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Set_Loop(Iterations=3){")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=1)")
            addEffect("	Goto(Unknown=-62)")
            addEffect("}")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Set_Loop(Iterations=2){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-64)")
            addEffect("}")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0xC0E00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F4EB852, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x40B00000, unknown=0x40E00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F4EB852, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=39)")
            addEffect("Script_End()")
            return True
    if char == "pitb":
        if move == "dude":
            return True
    if char == "donkey":
        if move == "SpecialAirHi.acm":
            addEffect(asynchronousTimer.format('3'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0xC0E00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F3B4396, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F3B4396, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=12)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown=0x16, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown=0x10, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)")
            addEffect("Set_Loop(Iterations=4){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x10, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x10, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB3F7CF, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB3F7CF, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=8)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-64)")
            addEffect("}")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000031, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=44)")
            addEffect("Set_Loop(Iterations=2){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x10, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x10, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB3F7CF, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB3F7CF, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=8)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-64)")
            addEffect("}")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "gamewatch":
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=2)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40A00000, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F733333, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40A00000, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F733333, unknown=0x1, unknown=0x437F0000, unknown=0x437F0000, unknown=0x437F0000)")
            addEffect(asynchronousTimer.format('5'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=9)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x404CCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=11)")
            addEffect("Asynchronous_Timer(Frames=14)")
            addEffect(terminateOverlays)
            addEffect("Asynchronous_Timer(Frames=26)")
            addEffect("Asynchronous_Timer(Frames=30)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=33)")
            addEffect("Script_End()")
            return True
    if char == "ness":
        if move == "SpecialAirHi.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x3F000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Set_Loop(Iterations=5){")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Goto(Unknown=-2)")
            addEffect("}")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x2, unknown=0x0, unknown=0x3F000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EE978D5, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=33)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    #check
    if char == "robot":
        if move == "SpecialHi.acm":
            addDodgeEffects2(['2','4'])
            return True
    if char == "gekkouga":
        if move == "SpecialLwHit.acm":
            addDodgeEffects2(['1', '37'])
            return True
    if char == "purin":
        if move == "SpecialLwL.acm":
            addEffect(asynchronousTimer.format('1'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=2)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0xD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA56042, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=3)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(asynchronousTimer.format('28'))
            addEffect(terminateOverlays)
            addEffect("Script_End()")
            return True
    if char == "kirby":
        if move == "SpecialSMax.acm":
            addEffect(asynchronousTimer.format('2'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect("Color_Overlay(Red=255, Green=0, Blue=255, Alpha=128)")
            addEffect("Asynchronous_Timer(Frames=11)")
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40866666, unknown=0x41380000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40866666, unknown=0x40B00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EBDB22D, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Overlays()")
            addEffect("Asynchronous_Timer(Frames=56)")
            addEffect("Script_End()")
            return True
    if char == "littlemac":
        if move == "SpecialHiStart.acm":
            addEffect(asynchronousTimer.format('1'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=3)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40DB6DB7, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40F6DB6E, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41092492, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4116DB6E, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41249249, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41324925, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40A00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41300000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=4)")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialLwHit.acm":
            addEffect(asynchronousTimer.format('1'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=15)")
            addEffect("Asynchronous_Timer(Frames=16)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=19)")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x40400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x4076DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x4096DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x40B24925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x40CDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x40E92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x41024925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41100000, unknown=0x41100000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=22)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "lucas":
        if move == "SpecialAirHi.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F5AE148, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x40400000, unknown=0xC0400000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F5AE148, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            # hit 1
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBE924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0249249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0524925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            # hit 2
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBE924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0249249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0524925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            # hit 3
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBE924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0249249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0524925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            # remove intangibility then hit 4
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBE924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0249249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0524925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            # hit 5
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBE924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ED126E9, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0249249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0524925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")

            addEffect("Set_Loop(Iterations=5){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBE924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF36DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3E924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBEDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBF924925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xBFEDB6DB, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0249249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0524925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F0A9FBE, unknown=0x1, unknown=0x437F0000, unknown=0x434F0000, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Synchronous_Timer(Frames=1)")
            addEffect("	Goto(Unknown=-38)")
            addEffect("}")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x3F800000, unknown=0xBF800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F91EB85, unknown=0x1, unknown=0x437F0000, unknown=0x42995555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "lucina":
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=4)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x41000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=12)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialAirHi.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x41000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=12)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "luigi":
        if move == "0x2A81E865.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x12, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect(asynchronousTimer.format('6'))
            addEffect(terminateOverlays)
            addEffect("Asynchronous_Timer(Frames=14)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=25)")
            addEffect("Script_End()")
            return True
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x40E00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E560419, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Subroutine(Hash=0x1A201091)")
            addEffect("Script_End()")
            return True
        if move == "SpecialAirHi.acm":
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Color_Overlay(Red=0, Green=0, Blue=255, Alpha=128)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x40E00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E560419, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Subroutine(Hash=0x1A201091)")
            addEffect("Script_End()")
            return True
        if move == "0x1A201091.acm":
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x13, unknown=0x0, unknown=0x404CCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F3AC711, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x4099999A, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F17C1BE, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(terminateOverlays)
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Asynchronous_Timer(Frames=10)")
            addEffect("Asynchronous_Timer(Frames=24)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "mario":
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=3)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x41100000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(terminateOverlays)
            addEffect("Set_Loop(Iterations=3){")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41080000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=1)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-34)")
            addEffect("}")
            addEffect("Set_Loop(Iterations=2){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41080000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3ECC49BA, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-36)")
            addEffect("}")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F733333, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41080000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F733333, unknown=0x1, unknown=0x437F0000, unknown=0x43380000, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "marth":
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=4)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x41000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=12)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialAirHi.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x41000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(terminateOverlays)
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42755555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x0, unknown=0x0, unknown=0xBFC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3, unknown=0x0, unknown=0x0, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=12)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialLwHit.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x3F800000, unknown=0x0, unknown=0x3FC00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0xE, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x3EA, unknown=0x3F800000, unknown=0x0, unknown=0x40E00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=8)")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        ## CHECK UP B
    if char == "pikachu:":
        if move == "LandingAirB.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F428F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(colorOverlay.format(*GREEN))
            addEffect(asynchronousTimer.format('31'))
            addEffect(terminateOverlays)
            addEffect("Script_End()")
            return True
        if move == "LandingAirLw.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0xC0000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x40000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40800000, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(colorOverlay.format(*GREEN))
            addEffect(asynchronousTimer.format('41'))
            addEffect(terminateOverlays)
            addEffect("Script_End()")
            return True
        if move == "SpecialLwHit.acm":
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41233333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F9E147B, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=3)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(synchronousTimer.format('8'))
            addEffect(terminateOverlays)
            addEffect("Script_End()")
            return True
    if char == "ryu":
        if move == "SpecialHi.acm":
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown=0x16, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown=0x15, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)")
            addEffect("Asynchronous_Timer(Frames=3)")
            addEffect("Color_Overlay(Red=0, Green=0, Blue=255, Alpha=128)")
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(terminateOverlays)
            addEffect("unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x2)")
            addEffect("TRUE(Unknown=0x10){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40F33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x41F55555, unknown=0x0)")
            addEffect("}")
            addEffect("FALSE(Unknown=0x1a){")
            addEffect("	unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x1)")
            addEffect("	TRUE(Unknown=0x16){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40F33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x41755555, unknown=0x0)")
            addEffect("	}")
            addEffect("	FALSE(Unknown=0x14){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40F33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("	}")
            addEffect("}")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x2)")
            addEffect("TRUE(Unknown=0x16){")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x17, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect("}")
            addEffect("FALSE(Unknown=0x1a){")
            addEffect("	unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x1)")
            addEffect("	TRUE(Unknown=0x16){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x17, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect("	}")
            addEffect("	FALSE(Unknown=0x14){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x17, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect("	}")
            addEffect("}")
            addEffect("Asynchronous_Timer(Frames=9)")
            addEffect("unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x2)")
            addEffect("TRUE(Unknown=0x16){")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0xBECCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("}")
            addEffect("FALSE(Unknown=0x1a){")
            addEffect("	unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x1)")
            addEffect("	TRUE(Unknown=0x16){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0xBECCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("	}")
            addEffect("	FALSE(Unknown=0x14){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0xBECCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("	}")
            addEffect("}")
            addEffect("Asynchronous_Timer(Frames=15)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000031, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=20)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "0x73CD97DF.acm":
            addEffect("Asynchronous_Timer(Frames=1)")
            addEffect("Color_Overlay(Red=0, Green=0, Blue=255, Alpha=128)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown=0x16, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown=0x15, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)")
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect("unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x2)")
            addEffect("TRUE(Unknown=0x10){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40F33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x41F55555, unknown=0x0)")
            addEffect("}")
            addEffect("FALSE(Unknown=0x1a){")
            addEffect("	unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x1)")
            addEffect("	TRUE(Unknown=0x16){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40F33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x41755555, unknown=0x0)")
            addEffect("	}")
            addEffect("	FALSE(Unknown=0x14){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41200000, unknown=0x40F33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("	}")
            addEffect("}")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(terminateOverlays)
            addEffect("unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x2)")
            addEffect("TRUE(Unknown=0x16){")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x17, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect("}")
            addEffect("FALSE(Unknown=0x1a){")
            addEffect("	unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x1)")
            addEffect("	TRUE(Unknown=0x16){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x17, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect("	}")
            addEffect("	FALSE(Unknown=0x14){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x17, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect("	}")
            addEffect("}")
            addEffect("Asynchronous_Timer(Frames=9)")
            addEffect("unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x2)")
            addEffect("TRUE(Unknown=0x16){")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0xBECCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("}")
            addEffect("FALSE(Unknown=0x1a){")
            addEffect("	unk_477705C2(unknown=0x11000002, unknown=0x0, unknown=0x1)")
            addEffect("	TRUE(Unknown=0x16){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0xBECCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F05C28F, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("	}")
            addEffect("	FALSE(Unknown=0x14){")
            addEffect("		Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "		EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0xBECCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x42F55555, unknown=0x0)")
            addEffect("	}")
            addEffect("}")
            addEffect("Asynchronous_Timer(Frames=15)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000031, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=20)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "rockman":
        if move == "AttackHi3.acm":
            addEffect(asynchronousTimer.format('5'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=6)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40C00000, unknown=0x41000000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E733333, unknown=0x1, unknown=0x437F0000, unknown=0x0, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=7)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42380000, unknown=0x0)")
            addEffect(asynchronousTimer.format('8'))
            addEffect(terminateOverlays)
            addEffect("Asynchronous_Timer(Frames=10)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x16, unknown=0x40900000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=17)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialHi.acm":
            addEffect(asynchronousTimer.format('6'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect(asynchronousTimer.format('10'))
            addEffect(terminateOverlays)
            return True
    if char == "roy":
        if move == "SpecialHi.acm":
            addEffect("Asynchronous_Timer(Frames=4)")
            addEffect("Color_Overlay(Red=255, Green=0, Blue=255, Alpha=128)")
            addEffect("Asynchronous_Timer(Frames=9)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41300000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x411AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41055555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41300000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x411AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41055555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF81062, unknown=0x1, unknown=0x437F0000, unknown=0x4311AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Overlays()")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43552222, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F00E560, unknown=0x1, unknown=0x437F0000, unknown=0x43552222, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43552222, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F00E560, unknown=0x1, unknown=0x437F0000, unknown=0x43552222, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=14)")
            addEffect("Asynchronous_Timer(Frames=20)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41755555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x415AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43552222, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F00E560, unknown=0x1, unknown=0x437F0000, unknown=0x43552222, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41755555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x415AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F1E147B, unknown=0x1, unknown=0x437F0000, unknown=0x42D6AAAB, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialAirHi.acm":
            addEffect("Asynchronous_Timer(Frames=9)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41300000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x411AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41055555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41300000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x411AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41055555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40E00000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EDFBE77, unknown=0x1, unknown=0x437F0000, unknown=0x43210000, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=10)")
            addEffect(terminateOverlays)
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F083127, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F083127, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Asynchronous_Timer(Frames=14)")
            addEffect("Asynchronous_Timer(Frames=20)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41755555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x415AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F083127, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41880000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41755555, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x415AAAAB, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41400000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F19374C, unknown=0x1, unknown=0x437F0000, unknown=0x430A0000, unknown=0x0)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "samus":
        if move == "SpecialHi.acm":
            addEffect(asynchronousTimer.format('3'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF99999A, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB8D4FE, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF99999A, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB8D4FE, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB8D4FE, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EB8D4FE, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(synchronousTimer.format('1'))
            addEffect(terminateOverlays)
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Set_Loop(Iterations=3){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xC0A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x3FD55555, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xBFD55555, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xC0A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-62)")
            addEffect("}")
            addEffect("Set_Loop(Iterations=6){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xC0A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x3FD55555, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xBFD55555, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xC0A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-64)")
            addEffect("}")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F6978D5, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
        if move == "SpecialAirHi.acm":
            addEffect(asynchronousTimer.format('3'))
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=5)")

            # hit 1
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E8D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E8D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF4CCCCD, unknown=0x40B33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA08312, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF4CCCCD, unknown=0xC0B33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA08312, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect(terminateOverlays)
            addEffect(synchronousTimer.format('1'))
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            # hit 2
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E8D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E8D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF4CCCCD, unknown=0x40B33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA08312, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF4CCCCD, unknown=0xC0B33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA08312, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            # hit 3
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0x40C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E8D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x4119999A, unknown=0xC0C00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3E8D0E56, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF4CCCCD, unknown=0x40B33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA08312, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0xBF4CCCCD, unknown=0xC0B33333, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EA08312, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")


            addEffect("Set_Loop(Iterations=8){")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xC0A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EAA3D71, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x40A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0x3FD55555, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xBFD55555, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "	EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40D00000, unknown=0xC0A00000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("	Synchronous_Timer(Frames=2)")
            addEffect("	Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("	Goto(Unknown=-50)")
            addEffect("}")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x40A66666, unknown=0x3FCCCCCD, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F6978D5, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=2)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Script_End()")
            return True
    if char == "sheik":
        if move == "SpecialLw.acm":
            addDodgeEffects2(['3','4'])
            return True
        if move == "SpecialAirLw.acm":
            addDodgeEffects2(['3','4'])
            return True
    if char == "murabito":
        if move == "SpecialN.acm":
            addDodgeEffects2(['5','23'])
            return True
    if char == "zelda":
        if move == "SpecialN.acm":
            addEffect("Asynchronous_Timer(Frames=5)")
            addEffect(colorOverlay.format(*BLUE))
            addEffect("Asynchronous_Timer(Frames=13)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC036DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xBFDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xBF124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x3FDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x4036DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F11EB85, unknown=0x1, unknown=0x437F0000, unknown=0x43475555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC1200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC0E49249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC0892492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xBFB6DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x3FB6DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40892492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40E49249, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x41200000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EC28F5C, unknown=0x1, unknown=0x437F0000, unknown=0x4356AAAB, unknown=0x0)")
            addEffect(asynchronousTimer.format('16'))
            addEffect(terminateOverlays)
            addEffect("Asynchronous_Timer(Frames=25)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=28)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC0800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC036DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xBFDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xBF124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x3F124925, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x3FDB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x4036DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40800000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3F2A3D71, unknown=0x1, unknown=0x437F0000, unknown=0x43195555, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC1300000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC0FB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xC096DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0xBFC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x3FC92492, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x4096DB6E, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x40FB6DB7, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect(
                "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown=0x0, unknown=0x0, unknown=0x41000000, unknown=0x41300000, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3EF33333, unknown=0x1, unknown=0x437F0000, unknown=0x4328AAAB, unknown=0x0)")
            addEffect("Synchronous_Timer(Frames=1)")
            addEffect("Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)")
            addEffect("Asynchronous_Timer(Frames=43)")
            addEffect("Script_End()")
            return True
    ''' 
    TODO:
     pitb
     metaknight
     pit
     reflet
     sonic spindash (in FITX v2.0)
    '''
    return False

main()

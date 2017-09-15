import os, sys, struct, subprocess, shlex, glob, shutil, math
from collections import OrderedDict

counterChars = "gekkouga,ike,kamui,littlemac,lucario,lucina,marth,palutena,peach,roy,shulk".split(",")

# game code lines
asynchronousTimer = "Asynchronous_Timer(Frames={})"
synchronousTimer = "Synchronous_Timer(Frames={})"
setBoneIntangability = "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)"
setHurtbox = "Graphic_Effect6(Graphic=0x1000031, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
setHurtboxIntang = "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)"
setHurtboxTest = "Graphic_Effect6(Graphic={}, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
showAngle = "Graphic_Effect6(Graphic=0x1000094, Bone=0x0, Z={}, Y={}, X={}, ZRot={}, YRot=0, XRot=0, Size=0.5, Terminate=0x1, Unknown=0x420C0000)"
grayHitbox = "Graphic_Effect6(Graphic=0x1000013, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
coloredHitbox = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown={}, unknown={}, unknown={})"
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
setFrameDuration = "Set_Frame_Duration(Speed={})"
ifCompare = "If_Compare(Variable={}, Method={}, Variable2={})"
ifCompare2 = "If_Compare2(Variable={}, Method={}, Value={})"
ifBitIsSet = "If_Bit_is_Set(Variable={})"
isExistArticle = "IS_EXIST_ARTICLE(Unknown={})"
basicCompare = "unk_477705C2(unknown={}, unknown={}, unknown={})"
floatCompare = "unk_2DA7E2B6(unknown={}, unknown={}, unknown={})"
TRUEComp = "TRUE(Unknown={}){{"
TRUEComp2 = "unk_870CF021(unknown={}){{"
FALSEComp = "FALSE(Unknown={}){{"
bitVariableSet = "Bit_Variable_Set(Variable={})"
bitVariableClear = "Bit_Variable_Clear(Variable={})"
basicVariableSet = "Basic_Variable_Set(Value={}, Variable={})"
floatVariableSet = "Float_Variable_Set(Value={}, Variable={})"
goto = "Goto(Unknown={})"
endLoopOrCompare = "}"
scriptEnd = "Script_End()"

# colors: R, G, B, Alpha
ALPHA = '128'

PINK = ['255', '105', '180', ALPHA]
RED = ['255', '0', '0', ALPHA]
ORANGE = ['255', '165', '0', ALPHA]
YELLOW = ['255', '255', '0', ALPHA]
GREEN = ['0', '255', '0', ALPHA]
BLUE = ['0', '0', '255', ALPHA]
CYAN = ['0', '255', '255', ALPHA]
MAGENTA = ['255', '0', '255', ALPHA]
TEAL = ['0', '128', '128', ALPHA]
TURQUOISE = ['64', '224', '208', ALPHA]
WHITE = ['255', '255', '255', ALPHA]
BLACK = ['0', '0', '0', ALPHA]

equalTo = "0x0"
notEqualTo = "0x1"
lessThanOrEqualTo = "0x2"
greaterThanOrEqualTo = "0x3"
###???
lessThan = "0x4"
greaterThan = "0x5"

# toggle 0: none; 1: fullMod+DI+hitstunOverlay; 2:DI+hitstunOverlay; 3: hitstunOverlay
showFullModVar = "0x1200004A" # brawl glide data param (originally 60)
hasEnteredVar = "0x1200004B" # brawl glide data param (originally 1)
mashToggleVar = "0x1200006E" # brawl cliffclimb over 100% (originally 100)
DIChangeVar = "0x2000126" # brawl max kb to execute momentum commands (originally 0.2)
DIDirectionVar = "0x2000127" # brawl (originally )
maxDIChange = 0.17
canAttackVar = "0x21000025"
canAirdodgeVar = "0x21000026"
shieldDegenVar = "0x20000C7"
shieldRegenVar = "0x20000C8"
shieldDamageMultVar = "0x20000CA"
extraVar = "0x21000028"
hitstunVar = "0x1000003E"
launchSpeedVar = "0x10000003" # launch speed basic
ourLaundSpeedBitVar = "0x21000027" # some other ryu thing

shouldProcessVariables = False
wifiSafe = False

effectLines = "\tEffect()\n\t{\r\n"
variableEffectLines = ""
damageEffectLines = ""
mainList = []
myLines = []
origEffectLines = ""
origIndex = 0
blacklisted = False
trainingOnly = False
weaponBool = False
inLoop = False
inCompare = 0
FAF = 10000
invStart = 10000
invEnd = 10000
# hurtboxes: hurtboxNum : attrList [X, ...}
hurtboxes = {}
currentFrame = 0

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def addHitstunOverlays(spinning=False):
    global damageEffectLines, effectLines, inCompare, inLoop
    if damageEffectLines == "":
        effectLines = "\tEffect()\n\t{\r\n"
        addEffect(basicCompare.format(showFullModVar, greaterThanOrEqualTo, hex(1)))
        addEffect(TRUEComp.format("0x12"))
        inCompare += 1
        addEffect(bitVariableClear.format(ourLaundSpeedBitVar))
        addEffect(bitVariableClear.format(canAttackVar))
        addEffect(bitVariableClear.format(canAirdodgeVar))
        # if facing right? check directions.
        addEffect(ifCompare.format("0x0", "0x4", "0x0"))
        addEffect(TRUEComp.format("0x12"))
        inCompare+=1
        addEffect(floatVariableSet.format(1.0, DIDirectionVar))
        inCompare-=1
        addEffect("}")
        addEffect(FALSEComp.format("0x10"))
        inCompare+=1
        addEffect(floatVariableSet.format(-1.0, DIDirectionVar))
        inCompare-=1
        addEffect("}")
        for i in range(1, 150):
            addEffect(asynchronousTimer.format(i))

            # 1 tab
            addEffect(basicCompare.format(hitstunVar, greaterThanOrEqualTo, hex(1)))
            addEffect(TRUEComp.format("0x12"))
            inCompare = inCompare + 1
            # 2 tabs
            addEffect(ifBitIsSet.format(ourLaundSpeedBitVar))
            addEffect(TRUEComp.format("0x12"))
            inCompare += 1
            # 3 tabs
            addEffect(ifBitIsSet.format(canAttackVar))
            addEffect(TRUEComp.format("0x12"))
            inCompare += 1
            addEffect(colorOverlay.format(*MAGENTA))
            inCompare -= 1
            addEffect("}")
            # 3 tabs
            addEffect(FALSEComp.format("0x10"))
            inCompare += 1
            # 4 tabs
            addEffect(ifBitIsSet.format(canAirdodgeVar))
            addEffect(TRUEComp.format("0x12"))
            inCompare += 1
            addEffect(colorOverlay.format(*CYAN))
            inCompare -= 1
            addEffect("}")
            addEffect(FALSEComp.format("0x10"))
            inCompare += 1
            if spinning:
                addEffect(colorOverlay.format(*ORANGE))
            else:
                addEffect(colorOverlay.format(*GREEN))
            inCompare -= 1
            addEffect("}")
            inCompare -= 1
            addEffect("}")
            # 2 tabs
            inCompare -= 1
            addEffect("}")
            addEffect(FALSEComp.format('0x10'))
            inCompare += 1
            # 3 tabs
            addEffect(basicCompare.format(hitstunVar, greaterThanOrEqualTo, hex(40)))
            addEffect(TRUEComp.format("0x12"))
            inCompare += 1
            addEffect(bitVariableSet.format(ourLaundSpeedBitVar))
            inCompare -= 1
            addEffect("}")
            addEffect(FALSEComp.format("0x10"))
            inCompare += 1
            if spinning:
                addEffect(colorOverlay.format(*ORANGE))
            else:
                addEffect(colorOverlay.format(*GREEN))
            inCompare -= 1
            addEffect("}")
            inCompare -= 1
            addEffect("}")
            inCompare = inCompare - 1
            addEffect("}")
            addEffect(FALSEComp.format("0x10"))
            inCompare = inCompare + 1
            addEffect(terminateOverlays)
            inCompare -= 1
            untilCompare = 2 if not wifiSafe else 0
            while inCompare > untilCompare:
                addEffect("}")
                inCompare = inCompare - 1
            addEffect("}")
        addEffect(scriptEnd)
        damageEffectLines = effectLines
    else:
        effectLines = damageEffectLines

def parseForEffect(lines):
    global origEffectLines
    inEffect = False
    for l in lines:
        if l.startswith("\t}"):
            inEffect = False
        if l.startswith("\tEffect()"):
            inEffect = True
        elif inEffect:
            if not l.startswith("\t\tScript_End()") and not l == "\t\tTRUE(Unknown=0x2)\r":
                origEffectLines = origEffectLines + "\t" + l + "\n"

def moreHitboxesExist(remainingLines):
    for i in remainingLines:
        if i.find("Hitbox") != -1 or i.find("Grab") != -1:
            return True
    return False

def moreTimersExist(remainingLines):
    for i in remainingLines:
        if i.find('}') != -1:
            return False
        if i.find("Synchronous_Timer") != -1 or i.find("Asynchronous_Timer") != -1:
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
        if FAF != 10000:
            addEffect(colorOverlay.format(*GREEN))
            return True
    #if blacklisted:
    #    effectLines = "\t\t" + scriptEnd + "\r\n"
    return False

def addHurtboxes():
    for hurtb in hurtboxes:
        h = hurtboxes[hurtb]
        xinit = float(h[0])
        yinit = float(h[1])
        zinit = float(h[2])
        xfinal = float(h[3])
        yfinal = float(h[4])
        zfinal = float(h[5])
        size = getHexFloat(float(h[6])) #* 19 / 200
        bone = hex(int(h[7]))
        for j in range(0, 4):
            zcurr = getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
            ycurr = getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
            xcurr = getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
            addEffect(setHurtbox.format(bone, xcurr, ycurr, zcurr, size))

def addHurtboxIntangibility(givenBone):
    for hurtb in hurtboxes:
        h = hurtboxes[hurtb]
        xinit = float(h[0])
        yinit = float(h[1])
        zinit = float(h[2])
        xfinal = float(h[3])
        yfinal = float(h[4])
        zfinal = float(h[5])
        size = getHexFloat(float(h[6])) #* 19 / 200
        size = '0x3FC00000' # default size until I get a better graphic
        bone = hex(int(h[7]))
        if bone == hex(int(givenBone, 16)):
            for j in range(0, 4):
                zcurr = getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
                ycurr = getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
                xcurr = getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
                addEffect(setHurtboxIntang.format(bone, xcurr, ycurr, zcurr, size))

def floatToHex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def getHexFloat(value):
    hexFloat = str(floatToHex(value)).upper()
    return "".join(c.lower() if (c == "X") else c for i, c in enumerate(hexFloat))

def getParamList(line):
    parameters = line[line.find("(") + 1:line.find(")")]
    fullParamList = parameters.split(',')
    paramList = [x[x.find("=") + 1:] for x in fullParamList]
    return paramList

def addListToMain(index):
    global myLines, origIndex
    origIndex = index
    addEffect(terminateGraphic13)
    for h in mainList:
        inserted = "\t\t" + h
        index = index + 1
        myLines.insert(index, inserted)
    return

def addToMainList(line,index):
    global mainList
    lineFound = False
    for h in mainList:
        if h == line:
            lineFound = True
    if removeFromMainList(getParamList(line)[0]):
        mainList.append(line)
        if not lineFound:
            addListToMain(index)
    else:
        mainList.append(line)

def addMovedToMainList(line,index):
    global mainList
    newLine = ""
    for h in mainList:
        if getParamList(h)[0] == getParamList(line)[0]:
            newLine = h
            removeFromMainList(getParamList(h)[0])
    boneIndex = newLine.find("Bone=")
    commaIndex = newLine[boneIndex:].find(",")
    newBone = getParamList(line)[1]
    newBoneStr = "Bone={}".format(newBone)
    newLine = newLine[:boneIndex] + newBoneStr + newLine[boneIndex+commaIndex:]
    xIndex = newLine.find("X=")
    commaIndex = newLine[xIndex:].find(",")
    newX = float(getParamList(line)[2])
    newXStr = "X={}".format(newX)
    newLine = newLine[:xIndex] + newXStr + newLine[xIndex + commaIndex:]
    yIndex = newLine.find("Y=")
    commaIndex = newLine[yIndex:].find(",")
    newY = float(getParamList(line)[3])
    newYStr = "Y={}".format(newY)
    newLine = newLine[:yIndex] + newYStr + newLine[yIndex + commaIndex:]
    zIndex = newLine.find("Z=")
    commaIndex = newLine[zIndex:].find(",")
    newZ = float(getParamList(line)[4])
    newZStr = "Z={}".format(newZ)
    newLine = newLine[:zIndex] + newZStr + newLine[zIndex + commaIndex:]
    mainList.append(newLine)

def addChangedToMainList(line,index):
    global mainList
    newLine = ""
    for h in mainList:
        if getParamList(h)[0] == getParamList(line)[0]:
            newLine = h
            removeFromMainList(getParamList(h)[0])
    sizeIndex = newLine.find("Size=")
    commaIndex = newLine[sizeIndex:].find(",")
    newSize = float(getParamList(line)[1]) # already been processed: * 19 / 200
    newSizeStr = "Size={}".format(newSize)
    newLine = newLine[:sizeIndex] + newSizeStr + newLine[sizeIndex+commaIndex:]
    mainList.append(newLine)

def removeFromMainList(hitboxID):
    global mainList
    for h in mainList:
        if getParamList(h)[0] == hitboxID:
            mainList.remove(h)
            return True
    return False

def addEffect(effectString):
    global effectLines
    if effectString == scriptEnd and not shouldProcessVariables and not weaponBool and not wifiSafe:
        return
    effectLines = effectLines + "\t\t"
    tabs = inCompare
    if inLoop:
        tabs = tabs + 1
    for q in range(tabs):
        effectLines = effectLines + "    "

    effectLines = effectLines + effectString + "\r\n"

def addEffectToString(effectString, string):
    if effectString == scriptEnd and not shouldProcessVariables and not weaponBool and not wifiSafe:
        return string
    string = string + "\t\t"
    tabs = inCompare
    if inLoop:
        tabs = tabs + 1
    for q in range(tabs):
        string = string + "    "

    string = string + effectString + "\r\n"
    return string

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

def getOutput(lines):
    inEffect = False
    fullOutput = ""
    for i in lines:
        if i == "\tEffect()\n\t{\r":
            inEffect = True
            fullOutput += effectLines + "\t}\n\r\n"
        if not inEffect:
            if i != "\t\tTRUE(Unknown=0x2)\r":
                fullOutput += i + "\n"
        else:
            if i == "\t}\n\r":
                inEffect = False
    return fullOutput

def getTrainingOutput(lines):
    inEffect = False
    fullOutput = ""
    for i in lines:
        if i == "\tEffect()\n\t{\r":
            inEffect = True
            if blacklisted:
                fullOutput += "\tEffect()\n\t{\r"
            fullOutput += effectLines
            fullOutput += origEffectLines+ "\t\t}\r\n\t\tScript_End()\r\n\t}\n\r\n"
        if not inEffect:
            if i != "\t\tTRUE(Unknown=0x2)\r":
                fullOutput += i + "\n"
        else:
            if i == "\t}\n\r":
                inEffect = False
    return fullOutput

def getBlacklistedOutput(lines):
    inEffect = False
    global effectLines
    fullOutput = ""
    if effectLines == "\tEffect()\n\t{\r\n":
        effectLines = effectLines + "\t}\n\r\n"
    for i in lines:
        if i == "\tEffect()\n\t{\r":
            inEffect = True
        if not inEffect:
            if i != "\t\tTRUE(Unknown=0x2)\r":
                fullOutput += i + "\n"
        else:
            if i == "\t\tScript_End()\r":
                fullOutput += effectLines
                inEffect = False
            elif i == "\t}\n\r":
                fullOutput += i + "\n"
                inEffect = False
            else:
                fullOutput += i + "\n"
    return fullOutput

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
    if isInt(lagLength):
        addEffect(asynchronousTimer.format("1"))
        addEffect(colorOverlay.format(*GREEN))
        addEffect(asynchronousTimer.format(str(int(lagLength) + 1)))
        addEffect(terminateOverlays)
    addEffect(scriptEnd)

def processFile(filePath, isBlacklisted=False, isTrainingOnly=False, isWeapon=False):
    global effectLines, inLoop, inCompare
    global blacklisted, trainingOnly, weaponBool
    global currentFrame, FAF, invStart, invEnd
    global myLines, mainList, origEffectLines

    weaponBool = isWeapon

    filename = filePath
    basename = os.path.basename(filename)

    # custom section
    shouldProcessCustom = False
    if shouldProcessCustom:
        if basename.startswith("FuraFuraStart"):
            addEffect(floatVariableSet.format(15, "0x1000006"))
            weaponBool = True
            addEffect(scriptEnd)
            return getOutput(lines)

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
    hitstunAnimations = {"DamageAir1.acm", "DamageAir2.acm", "DamageAir3.acm", "DamageElec.acm", "DamageFlyHi.acm", "DamageFlyLw.acm", "DamageFlyN.acm", "DamageFlyTop.acm", "DamageHi1.acm", "DamageHi2.acm", "DamageHi3.acm", "DamageLw1.acm", "DamageLw2.acm", "DamageLw3.acm", "DamageN1.acm", "DamageN2.acm", "DamageN3.acm", "WallDamage.acm"}
    upTaunts = {"AppealHiL.acm", "AppealHiR.acm"}
    sideTaunts = {"AppealSL.acm", "AppealSR.acm"}
    downTaunts = {"AppealLwL.acm", "AppealLwR.acm"}
    tumble = "DamageFall.acm"
    specialFall = "FallSpecial.acm"
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

    if isBlacklisted:
        blacklisted = True
        effectLines = ""

    if isTrainingOnly:
        if basename in {"EntryR.acm", "EntryL.acm"}:
            addEffect(basicVariableSet.format("0x0", showFullModVar))
            addEffect(basicVariableSet.format("0x0", hasEnteredVar))

    if not shouldProcessVariables and not weaponBool and not wifiSafe:
        trainingOnly = True
        if basename in upTaunts or basename.startswith("Wait"):
            addEffect(basicCompare.format(hasEnteredVar, notEqualTo, "0x0"))
        elif basename in sideTaunts or basename in downTaunts:
            addEffect(basicCompare.format(showFullModVar, greaterThanOrEqualTo, "0x1"))
            addEffect(TRUEComp.format("0x12"))
            inCompare += 1
            addEffect(basicCompare.format(showFullModVar,lessThanOrEqualTo, "0x2"))
        else:
            addEffect(basicCompare.format(showFullModVar, equalTo, "0x1"))
        addEffect(TRUEComp.format("0x12"))
        inCompare += 1

    with open(filename, newline="\r\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]
    if trainingOnly:
        parseForEffect(lines)
    for l in lines:
        myLines.append(l)

    inMain = False
    shouldExitLoop = False
    gotoNum = 0
    offsetBegin = 0
    offsetEnd = 0
    prevFrame = 0
    processedEndlag = False

    tsvLines = []

    # tsvData found in TSV folder; read any file for example layout
    charName = os.path.split(os.path.dirname(filename))[0][:-5]
    if charName[-4:] == "body":
        charName = charName[:-4]
        tsvPath = "TSV/{}.tsv".format(charName)
        if os.path.isfile(tsvPath):
            with open(tsvPath) as tsv:
                for line in tsv:
                    currMove = "\t" + basename[:-4] + "\t"
                    if currMove in line:
                        currFile = line.split('\t')
                        FAFIndex = 2
                        while not isInt(currFile[FAFIndex]):
                            FAFIndex = FAFIndex + 1
                        invStartIndex = FAFIndex + 1
                        invEndIndex = invStartIndex + 1
                        FAF = int(currFile[FAFIndex]) if int(currFile[FAFIndex]) != 0 else FAF
                        invStart = int(currFile[invStartIndex]) if int(currFile[invStartIndex]) != 0 else invStart
                        if int(currFile[invEndIndex]) != 0:
                            invStart = int(currFile[invStartIndex])
                            invEnd = int(currFile[invEndIndex])
                        if (charName in counterChars and basename == "SpecialLw.acm") or charName == "peach" and basename == "SpecialN.acm":
                            invStart = 10000
                            invEnd = 10000
                    tsvLines.append(line)
                # tsvLines = tsv.readlines()
            tsvLines = [x.strip('\n') for x in tsvLines]
            paramsIndex = tsvLines.index("PARAMS SECTION")
            hurtboxesIndex = tsvLines.index("BONES SECTION")

            for h in range(hurtboxesIndex+2,len(tsvLines)):
                currVals = tsvLines[h].split("\t")
                currHurtboxList = []
                for index in range(len(currVals)):
                    if index > 0:
                        currHurtboxList.append(currVals[index])
                hurtboxes[currVals[0]] = currHurtboxList

    # addHurtboxes()

    inputIndex = filename.find("Input")
    edgeCaseFilename = filename[:inputIndex] + filename[inputIndex+len("Input/animcmd/"):]

    if didHandleEdgeCase(edgeCaseFilename):
        pass
    elif basename.startswith("Wait") and not weaponBool:
        addEffect(basicCompare.format(showFullModVar, greaterThanOrEqualTo, hex(4)))
        addEffect(TRUEComp.format("0x12"))
        inCompare += 1
        addEffect(colorOverlay.format(*RED))
        addEffect(basicVariableSet.format(hex(1), showFullModVar))
        inCompare -= 1
        addEffect('}')
        addEffect(scriptEnd)
    elif basename in downTaunts and not weaponBool and not wifiSafe:
        mashDict = OrderedDict(
            [(0, RED), (1, GREEN), (2, BLUE), (3, WHITE)])
        numToggles = len(mashDict)
        addEffect(basicCompare.format(mashToggleVar, greaterThanOrEqualTo, hex(numToggles-1)))
        addEffect(TRUEComp.format("0x12"))
        inCompare += 1
        addEffect(colorOverlay.format(*RED))
        addEffect(basicVariableSet.format(hex(0), mashToggleVar))
        inCompare -= 1
        addEffect("}")
        addEffect(FALSEComp.format("0x10"))
        inCompare += 1
        for mashIndex in range(numToggles-1):
            currVal = mashIndex
            newVal = mashIndex+1
            color = mashDict[newVal]
            addEffect(basicCompare.format(mashToggleVar, equalTo, hex(currVal)))
            addEffect(TRUEComp.format("0x12"))
            inCompare += 1
            addEffect(basicVariableSet.format(hex(newVal), mashToggleVar))
            addEffect(colorOverlay.format(*color))
            if newVal == numToggles - 2:
                addEffect(floatVariableSet.format("0", shieldDamageMultVar))
                addEffect(floatVariableSet.format("0", shieldDegenVar))
                addEffect(floatVariableSet.format("0", shieldRegenVar))
            elif newVal == numToggles - 1:
                addEffect(floatVariableSet.format("1.19", shieldDamageMultVar))
                addEffect(floatVariableSet.format("0.13", shieldDegenVar))
                addEffect(floatVariableSet.format("0.08", shieldRegenVar))
            inCompare -= 1
            addEffect("}")
            addEffect(FALSEComp.format("0x10"))
            inCompare = inCompare + 1
        inCompare -= 1
        while inCompare > 1:
            addEffect("}")
            inCompare = inCompare - 1
        addEffect("}")
        addEffect(scriptEnd)
    elif basename in upTaunts and not weaponBool and not wifiSafe:
        effectToggleLines = ""
        effectToggleLines = addEffectToString(basicCompare.format(showFullModVar, equalTo, "0x0"), effectToggleLines)

        effectToggleLines = addEffectToString(TRUEComp.format("0x12"), effectToggleLines)
        inCompare += 1
        effectToggleLines = addEffectToString(colorOverlay.format(*RED), effectToggleLines)
        effectToggleLines = addEffectToString(basicVariableSet.format("0x1", showFullModVar), effectToggleLines)
        inCompare -= 1
        effectToggleLines = addEffectToString("}", effectToggleLines)
        effectToggleLines = addEffectToString(FALSEComp.format("0x10"), effectToggleLines)
        inCompare += 1
        effectToggleLines = addEffectToString(basicCompare.format(showFullModVar, equalTo, "0x1"), effectToggleLines)
        effectToggleLines = addEffectToString(TRUEComp.format("0x12"), effectToggleLines)
        inCompare += 1
        effectToggleLines = addEffectToString(colorOverlay.format(*GREEN), effectToggleLines)
        effectToggleLines = addEffectToString(basicVariableSet.format("0x2", showFullModVar), effectToggleLines)
        inCompare -= 1
        effectToggleLines = addEffectToString("}", effectToggleLines)
        effectToggleLines = addEffectToString(FALSEComp.format("0x10"), effectToggleLines)
        inCompare += 1
        effectToggleLines = addEffectToString(basicCompare.format(showFullModVar, equalTo, "0x2"), effectToggleLines)
        effectToggleLines = addEffectToString(TRUEComp.format("0x12"), effectToggleLines)
        inCompare += 1
        effectToggleLines = addEffectToString(colorOverlay.format(*BLUE), effectToggleLines)
        effectToggleLines = addEffectToString(basicVariableSet.format("0x3", showFullModVar), effectToggleLines)
        inCompare -= 1
        effectToggleLines = addEffectToString("}", effectToggleLines)
        effectToggleLines = addEffectToString(FALSEComp.format("0x10"), effectToggleLines)
        inCompare += 1
        effectToggleLines = addEffectToString(colorOverlay.format(*WHITE), effectToggleLines)
        effectToggleLines = addEffectToString(basicVariableSet.format("0x0", showFullModVar), effectToggleLines)
        inCompare -= 1
        effectToggleLines = addEffectToString("}", effectToggleLines)
        inCompare -= 1
        effectToggleLines = addEffectToString("}", effectToggleLines)
        inCompare -= 1
        effectToggleLines = addEffectToString("}", effectToggleLines)
        effectToggleLines = addEffectToString(scriptEnd, effectToggleLines)
        effectLines += effectToggleLines
    elif basename in sideTaunts and not weaponBool and not wifiSafe:
        # normal, 0,
        DIValues = [0.2, 0, 0.785398, 1.570796, 2.356194, 3.141593, -2.356194,  -1.570796, -0.785398,  10, 0.2]
        DIDict = OrderedDict(
            [(0.2, WHITE), (3.141593, BLACK), (2.356194, BLACK), (1.570796, BLACK), (0.785398, BLACK), (0, BLACK), (-0.785398, BLACK), (-1.570796, BLACK), (-2.356194, BLACK), (10, MAGENTA)])
        for DIindex in range(len(DIValues)-1):
            currVal = DIValues[DIindex]
            newVal = DIValues[DIindex+1]
            color = DIDict[newVal]
            addEffect(floatCompare.format(DIChangeVar, equalTo, getHexFloat(currVal)))
            addEffect(TRUEComp.format("0x12"))
            inCompare = inCompare + 1
            addEffect(floatVariableSet.format(newVal, DIChangeVar))
            addEffect(colorOverlay.format(*color))
            if color == BLACK:
                addEffect(showAngle.format(0,-30*math.sin(newVal)+10,30*math.cos(newVal),math.degrees(newVal)))
            inCompare = inCompare - 1
            addEffect("}")
            addEffect(FALSEComp.format("0x10"))
            inCompare = inCompare + 1
        inCompare -= 1
        while inCompare > 1:
            addEffect("}")
            inCompare = inCompare - 1
        addEffect("}")
    elif basename == spinningAnim:
        addHitstunOverlays(spinning=True)
    elif basename in hitstunAnimations:
        addHitstunOverlays()
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
    elif basename == tumble:
        addEffect(scriptEnd)
    elif basename == specialFall:
        addEffect(colorOverlay.format(*GREEN))
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
    elif basename == landingAirB:
        addLagEffects(tsvLines[21].split("\t")[0])
    elif basename == landingAirHi:
        addLagEffects(tsvLines[22].split("\t")[0])
    elif basename == landingAirLw:
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
            # removeLastEffect(scriptEnd)
        index = 0
        while index < len(myLines):
            iorig = myLines[index]
            i = removeBeginningWhitespace(iorig)

            # print(i)

            if i == "Main()\n\t{\r":
                inMain = True
                if myLines[index + 1] == "\t}\n\r":
                    break
            if shouldExitLoop:
                break
            if inMain:
                paramList = getParamList(i)

                if i.startswith("}"):
                    if inCompare:
                        if inCompare == 1 and trainingOnly:
                            if inLoop:
                                inLoop = False
                                addEffect(endLoopOrCompare)
                            else:
                                inMain = False
                                shouldExitLoop = True
                        else:
                            inCompare = inCompare - 1
                            addEffect(endLoopOrCompare)
                    elif inLoop:
                        inLoop = False
                        addEffect(endLoopOrCompare)
                    else:
                        inMain = False
                        shouldExitLoop = True

                if i.startswith("If_Compare2"):
                    addEffect(ifCompare2.format(paramList[0], paramList[1], paramList[2]))
                elif i.startswith("If_Compare"):
                    addEffect(ifCompare.format(paramList[0], paramList[1], paramList[2]))
                if i.startswith("If_Bit_is_Set"):
                    addEffect(ifBitIsSet.format(paramList[0]))
                if i.startswith("IS_EXIST_ARTICLE"):
                    addEffect(isExistArticle.format(paramList[0]))
                if i.startswith("unk_477705C2"):
                    addEffect(basicCompare.format(paramList[0], paramList[1], paramList[2]))
                if i.startswith("unk_2DA7E2B6"):
                    addEffect(floatCompare.format(paramList[0], paramList[1], paramList[2]))
                if i.startswith("TRUE"):
                    addEffect(TRUEComp.format(paramList[0]))
                    inCompare = inCompare + 1
                if i.startswith("unk_870CF021"):
                    addEffect(TRUEComp2.format(paramList[0]))
                    inCompare = inCompare + 1
                if i.startswith("FALSE"):
                    addEffect(FALSEComp.format(paramList[0]))
                    inCompare = inCompare + 1
                if i.startswith("Goto"):
                    addEffect(goto.format(-gotoNum))
                    gotoNum = 0

                loop = "Set_Loop"
                if i.startswith("Set_Loop"):
                    loopNum = int(paramList[0]) # if paramList[0] != "-1" else 0
                    addEffect(setLoop.format(loopNum))
                    inLoop = True

                if i.startswith("Loop_Rest()"):
                    addEffect("Loop_Rest()")

                if i.startswith("Set_Frame_Duration"):
                    addEffect(setFrameDuration.format(paramList[0]))

                if i.startswith("Set_Armor"):
                    state = paramList[0]
                    if state == "0x0":
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(*MAGENTA))

                if i.startswith("Body_Collision"):
                    state = paramList[0]
                    if state == "0x0":
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(*BLUE))

                if i.startswith("Search_Collision"):
                    bone = paramList[2]
                    size = getHexFloat(float(paramList[3]) * 19 / 200)
                    z = getHexFloat(float(paramList[4]))
                    y = getHexFloat(float(paramList[5]))
                    x = getHexFloat(float(paramList[6]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255)
                    addEffect(coloredHitbox.format(bone, z, y, x, size, red, green, blue))

                if i.startswith("Subroutine"):
                    hashNum = paramList[0]
                    addEffect(subroutine.format(hashNum))

                if i.startswith("External_Subroutine"):
                    hashNum = paramList[0]
                    addEffect(extsubroutine.format(hashNum))

                if i.startswith("WAIT_LOOP_CLR()"):
                    addEffect("WAIT_LOOP_CLR()")

                if i.startswith("Defensive_Collision"):
                    addEffect(colorOverlay.format(*RED))

                if i.startswith("Bit_Variable_Set"):
                    var = paramList[0]
                    specialLw = "SpecialLw"
                    if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                        addEffect(colorOverlay.format(*RED))

                if i.startswith("Bit_Variable_Clear"):
                    var = paramList[0]
                    specialLw = "SpecialLw"
                    if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                        addEffect(terminateOverlays)
                        if didProcessEndlag(myLines, index, basename, tsvLines):
                            processedEndlag = True

                if i.startswith("Terminate_Defensive_Collision"):
                    addEffect(terminateOverlays)
                    if didProcessEndlag(myLines, index, basename, tsvLines):
                        processedEndlag = True

                if i.startswith("Basic_Variable_Set"):
                    if offsetBegin == 0 and paramList[1] == "0x1100000F":
                        offsetBegin = int(paramList[0], 16)
                        prevFrame = int(getParamList(getLastEffectString())[0])
                        removeLastEffect(asynchronousTimer.format(prevFrame))
                        addEffect(asynchronousTimer.format(prevFrame + offsetBegin))
                    elif paramList[1] == "0x11000010":
                        offsetEnd = int(paramList[0], 16)

                if i.startswith("Asynchronous_Timer") and not processedEndlag:
                    currentFrame = int(paramList[0])
                    if currentFrame > FAF:
                        addEffect(asynchronousTimer.format(FAF))
                        addEffect(terminateOverlays)
                        FAF = 10000
                    if currentFrame > invStart:
                        addEffect(asynchronousTimer.format(invStart))
                        addEffect(colorOverlay.format(*BLUE))
                        invStart = 10000
                    if currentFrame > invEnd:
                        addEffect(asynchronousTimer.format(invEnd))
                        addEffect(terminateOverlays)
                        invEnd = 10000
                        if not moreHitboxesExist(myLines[index:]):
                            addEffect(colorOverlay.format(*GREEN))
                    if offsetEnd != 0:
                        addEffect(asynchronousTimer.format(offsetEnd + prevFrame))
                        addEffect(terminateGraphic13)
                        addEffect(asynchronousTimer.format(offsetBegin + int(paramList[0])))
                        prevFrame = int(paramList[0])
                    else:
                        addEffect(asynchronousTimer.format(paramList[0]))
                    if currentFrame == FAF:
                        addEffect(terminateOverlays)
                        FAF = 10000
                    if currentFrame == invStart:
                        addEffect(colorOverlay.format(*BLUE))
                        invStart = 10000
                    if currentFrame == invEnd:
                        addEffect(terminateOverlays)
                        invEnd = 10000
                        if not moreHitboxesExist(myLines[index:]):
                            addEffect(colorOverlay.format(*GREEN))
                elif i.startswith("Synchronous_Timer") and not processedEndlag:
                    if isInt(paramList[0]):
                        currentFrame = currentFrame + int(paramList[0])
                        frameToAdd = int(paramList[0])
                    else:
                        index = index + 1
                        continue
                    if currentFrame > FAF:
                        addEffect(asynchronousTimer.format(FAF))
                        addEffect(terminateOverlays)
                        frameToAdd = currentFrame - FAF
                        FAF = 10000
                    if currentFrame > invStart:
                        addEffect(asynchronousTimer.format(invStart))
                        addEffect(colorOverlay.format(*BLUE))
                        frameToAdd = currentFrame - invStart
                        invStart = 10000
                    if currentFrame > invEnd:
                        addEffect(asynchronousTimer.format(invEnd))
                        addEffect(terminateOverlays)
                        frameToAdd = currentFrame - invEnd
                        invEnd = 10000
                        if not moreHitboxesExist(myLines[index:]):
                            addEffect(colorOverlay.format(*GREEN))
                    addEffect(synchronousTimer.format(frameToAdd))
                    if currentFrame == FAF:
                        addEffect(terminateOverlays)
                        FAF = 10000
                    if currentFrame == invStart:
                        addEffect(colorOverlay.format(*BLUE))
                        invStart = 10000
                    if currentFrame == invEnd:
                        addEffect(terminateOverlays)
                        invEnd = 10000
                        if not moreHitboxesExist(myLines[index:]):
                            addEffect(colorOverlay.format(*GREEN))

                if i.startswith("Undo_Bone_Collision"):
                    addEffect(terminateGraphic31)

                if i.startswith("Enable Action Status") or i.startswith("Remove_All_Hitboxes"):
                    addEffect(terminateGraphic13)
                    mainList = []
                    if didProcessEndlag(myLines, index, basename, tsvLines):
                        processedEndlag = True

                if i.startswith("Terminate_Grab_Collisions"):
                    addEffect(terminateGraphic13)
                    mainList = []
                    if didProcessEndlag(myLines, index, basename, tsvLines):
                        processedEndlag = True

                if i.startswith("Delete_Catch_Collision"):
                    addEffect(terminateGraphic13)
                    if index != origIndex + len(mainList):
                        removeFromMainList(paramList[0])
                        addListToMain(index)
                    if didProcessEndlag(myLines, index, basename, tsvLines):
                        processedEndlag = True

                if i.startswith("Delete_Hitbox"):
                    addEffect(terminateGraphic13)
                    if index != origIndex + len(mainList):
                        removeFromMainList(paramList[0])
                        addListToMain(index)
                    if didProcessEndlag(myLines, index, basename, tsvLines):
                        processedEndlag = True

                if i.startswith("Set_Bone_Intangability"):
                    bone = paramList[0]
                    addHurtboxIntangibility(bone)

                if not blacklisted:
                    if i.startswith("Move_Hitbox"):
                        addMovedToMainList(i,index)
                        addEffect(terminateGraphic13)
                        addListToMain(index)

                    if i.startswith("Change_Hitbox_Size"):
                        addChangedToMainList(i,index)
                        addEffect(terminateGraphic13)
                        addListToMain(index)

                    if i.startswith("Hitbox") or i.startswith("Special_Hitbox") or i.startswith("Collateral_Hitbox"):
                        addToMainList(i,index)
                        bone = paramList[2]
                        size = getHexFloat(float(paramList[8]) * 19 / 200)
                        z = getHexFloat(float(paramList[9]))
                        y = getHexFloat(float(paramList[10]))
                        x = getHexFloat(float(paramList[11]))
                        red, green, blue = getDamageRGB(paramList[3], paramList[4])
                        addEffect(coloredHitbox.format(bone, z, y, x, size, red, green, blue))

                    if i.startswith("Extended_Hitbox"):
                        addToMainList(i,index)
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
                            addEffect(coloredHitbox.format(bone, zcurr, ycurr, xcurr, size, red, green, blue))

                    if i.startswith("Extended_Special_Hitbox"):
                        addToMainList(i,index)
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
                            addEffect(coloredHitbox.format(bone, zcurr, ycurr, xcurr, size, red, green, blue))

                if i.startswith("Grab_Collision2"):
                    addToMainList(i, index)
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    addEffect(grabHitbox.format(bone, z, y, x, size))
                elif i.startswith("Grab_Collision"):
                    addToMainList(i, index)
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    addEffect(grabHitbox.format(bone, z, y, x, size))

                if i.startswith("Extended_Grab_Collision"):
                    addToMainList(i, index)
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
                        addEffect(grabHitbox.format(bone, zcurr, ycurr, xcurr, size))

                if inLoop and not i.startswith("Set_Loop()"):
                    thisParamList = getParamList(getLastEffectString())
                    if thisParamList[0] != "":
                        gotoNum = gotoNum + len(thisParamList) + 1
                    else:
                        gotoNum = gotoNum + len(thisParamList)

                if i.startswith("Script_End()"):
                    if currentFrame < invStart and invStart != 10000:
                        addEffect(asynchronousTimer.format(invStart))
                        currentFrame = invStart
                        addEffect(terminateOverlays)
                        invStart = 10000
                    if currentFrame < invEnd and invEnd != 10000:
                        addEffect(asynchronousTimer.format(invEnd))
                        currentFrame = invEnd
                        addEffect(terminateOverlays)
                        addEffect(colorOverlay.format(*GREEN))
                        invEnd = 10000
                    if currentFrame < FAF and FAF != 10000:
                        addEffect(colorOverlay.format(*GREEN))
                        addEffect(asynchronousTimer.format(FAF))
                        currentFrame = FAF
                        addEffect(terminateOverlays)
                        FAF = 10000
                    if offsetBegin != 0:
                        addEffect(asynchronousTimer.format(prevFrame + offsetEnd))
                        addEffect(terminateGraphic13)
                    if not trainingOnly:
                        addEffect(scriptEnd)
                    inMain = False
                    shouldExitLoop = True
            index = index + 1

        if currentFrame < invStart and invStart != 10000:
            addEffect(asynchronousTimer.format(invStart))
            currentFrame = invStart
            addEffect(colorOverlay.format(*BLUE))
        if currentFrame < invEnd and invEnd != 10000:
            addEffect(asynchronousTimer.format(invEnd))
            currentFrame = invEnd
            addEffect(terminateOverlays)
            addEffect(colorOverlay.format(*GREEN))
        if currentFrame < FAF and FAF != 10000:
            addEffect(colorOverlay.format(*GREEN))
            addEffect(asynchronousTimer.format(FAF))
            currentFrame = FAF
            addEffect(terminateOverlays)
            FAF = 10000

    if trainingOnly:
        inCompare = 0
        addEffect("}")
        addEffect(FALSEComp.format("0x10"))
        return getTrainingOutput(lines)
    elif blacklisted:
        return getBlacklistedOutput(lines)
    else:
        return getOutput(lines)

def didHandleEdgeCase(filename):
    global inLoop, inCompare, shouldProcessVariables
    global variableEffectLines, effectLines, damageEffectLines

    # change "False" to "True" to test variables
    if not shouldProcessVariables:
        # special edge case: bayo up b not working in vanilla fix; doesn't work
        '''
        if filename == "bayonettabodySpecialHi.acm" and trainingOnly:
            effectLines = "\tEffect()\n\t{\r\n" + origEffectLines
            return True
        '''

        filepath = "edgeCaseCode/{}".format(filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.readlines()
            content = [x.strip('\n') for x in content]
            inEffect = False
            for line in content:
                #line = removeBeginningWhitespace(line)
                if line.startswith("\tEffect()"):
                    inEffect = True
                elif inEffect and not line.startswith("\t{") and not line.startswith("\t}"):
                    addEffect(line[1:])
                elif line.startswith("\t}"):
                    inEffect = False
            return True
    else:
        # variable testing
        basicVar = "0x100000AC"
        basicCompMethod = equalTo
        basicDict = OrderedDict(
            [(10, PINK), (6, RED), (5, ORANGE), (4, YELLOW), (3, GREEN), (2, BLUE), (1, CYAN), (0, MAGENTA)])
        floatVar = "0x2000218"
        floatCompMethod = "0x3"
        floatDict = OrderedDict([(6.28, PINK), (3.14, RED), (1.57, ORANGE), (0.785, YELLOW), (0, GREEN), (-0.785, BLUE), (-1.57, CYAN), (-3.14, MAGENTA)])
        bitVar = "0x21000025"
        whichToProcess = "float"
        tauntsOnly = False
        if tauntsOnly and filename.find("Appeal") == -1:
            return True
        if whichToProcess == "bit":
            # bit variables, frames 1 through 100
            if variableEffectLines == "":
                for i in range(1, 101):
                    addEffect(asynchronousTimer.format(i))
                    addEffect(ifBitIsSet.format(bitVar))
                    addEffect(TRUEComp.format("0x12"))
                    inCompare = inCompare + 1

                    addEffect(colorOverlay.format(*CYAN))

                    inCompare = inCompare - 1
                    addEffect("}")
                    addEffect(FALSEComp.format("0x10"))
                    inCompare = inCompare + 1
                    addEffect(colorOverlay.format(*RED))
                    inCompare -= 1
                    while inCompare:
                        addEffect("}")
                        inCompare = inCompare - 1
                    addEffect("}")
                addEffect(scriptEnd)
                variableEffectLines = effectLines
            else:
                effectLines = variableEffectLines
        elif whichToProcess == "float":
            # float variables, frames 1 through 100
            if variableEffectLines == "":
                for i in range(1, 101):
                    addEffect(asynchronousTimer.format(i))
                    for value in floatDict:
                        color = floatDict[value]
                        addEffect(floatCompare.format(floatVar, floatCompMethod, getHexFloat(value)))
                        addEffect(TRUEComp.format("0x12"))
                        inCompare = inCompare + 1

                        addEffect(colorOverlay.format(*color))

                        inCompare = inCompare - 1
                        addEffect("}")
                        addEffect(FALSEComp.format("0x10"))
                        inCompare = inCompare + 1
                    addEffect(colorOverlay.format(*WHITE))
                    inCompare -= 1
                    while inCompare:
                        addEffect("}")
                        inCompare = inCompare - 1
                    addEffect("}")
                addEffect(scriptEnd)
                variableEffectLines = effectLines
            else:
                effectLines = variableEffectLines
        elif whichToProcess == "basic":
            # basic variables
            if variableEffectLines == "":
                for i in range(1, 101):
                    addEffect(asynchronousTimer.format(i))
                    for value in basicDict:
                        color = basicDict[value]
                        addEffect(basicCompare.format(basicVar, basicCompMethod, hex(value)))
                        addEffect(TRUEComp.format("0x12"))
                        inCompare = inCompare + 1

                        addEffect(colorOverlay.format(*color))

                        inCompare = inCompare - 1
                        addEffect("}")
                        addEffect(FALSEComp.format("0x10"))
                        inCompare = inCompare + 1
                    addEffect(colorOverlay.format(*WHITE))
                    inCompare -= 1
                    while inCompare:
                        addEffect("}")
                        inCompare = inCompare - 1
                    addEffect("}")
                addEffect(scriptEnd)
                variableEffectLines = effectLines
            else:
                effectLines = variableEffectLines
        return True
    return False

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

def resetGlobals():
    global effectLines, inLoop, inCompare
    global blacklisted, trainingOnly
    global currentFrame, FAF, invStart, invEnd, hurtboxes
    global myLines, origIndex, mainList, origEffectLines
    effectLines = "\tEffect()\n\t{\r\n"
    mainList = []
    myLines = []
    origEffectLines = ""
    origIndex = 0
    blacklisted = False
    trainingOnly = False
    inLoop = False
    inCompare = 0
    FAF = 10000
    invStart = 10000
    invEnd = 10000
    hurtboxes = {}
    currentFrame = 0

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
            for filePath in files:
                resetGlobals()
                file = os.path.basename(filePath)
                stretchCheck = stretchChecker(char, bodyOrWeapon, file)
                if stretchCheck == "blacklisted":
                    print("Processing blacklisted file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    outputFile.write(processFile(filePath, isBlacklisted=True, isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    outputFile.close()
                else:
                    print("Processing file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    outputFile.write(processFile(filePath, isTrainingOnly=trainingMode, isWeapon=weaponBool))
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
            for file in files:
                resetGlobals()
                filePath = "{}/animcmd/{}".format(inputDir, file)
                stretchCheck = stretchChecker(char, bodyOrWeapon, file)
                if stretchCheck == "blacklisted":
                    print("Processing blacklisted file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    outputFile.write(processFile(filePath, isBlacklisted=True, isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    outputFile.close()
                elif stretchCheck == "noprocess":
                    print("Moving noprocess file {} for {}...".format(file, char))
                    shutil.copy(filePath, "{}/animcmd/{}".format(outputDir, file))
                else:
                    print("Processing file {} for {}...".format(file, char))
                    outputFile = open("{}/animcmd/{}".format(outputDir, file), 'w')
                    outputFile.write(processFile(filePath, isTrainingOnly=trainingMode, isWeapon=weaponBool))
                    outputFile.close()

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
    print(processFile(sys.argv[1], isBlacklisted=blklisted, isTrainingOnly=training))
else:
    main()

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
# effectString: [hitboxID, isDeleted]
effectStringDict = OrderedDict()

condList = []
hasParsed = False

inLoop = False
inCompare = 0


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
    if char == "sonic":
        if  move == "SpecialHi.acm":
            addDodgeEffects2(['5', '13'])
            removeLastEffect(scriptEnd)
            addEffect(asynchronousTimer.format('16'))
            addEffect(extsubroutine.format('0x3392B468'))
            addEffect(scriptEnd)
            return True
    return False

def parseForConditionals(lines):
    global condList, hasParsed
    if hasParsed:
        return
    inEffect = False
    for i in lines:
        if i == "\tEffect()\n\t{\r":
            inEffect = True
        if inEffect:
            if i[:len("\t\tTRUE")] == "\t\tTRUE" or i[:len("\t\tFALSE")] == "\t\tFALSE":
                condList.append(getParamList(i)[0])
            if i == "\t}\n\r":
                inEffect = False
    hasParsed = True

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
    addEffectID(effectString, -1)

def markAllHitboxesDeleted():
    for e in effectStringDict:
        effectStringDict[e][1] = 1

def addEffectID(effectString, hitboxID):
    global effectLines, effectStringDict
    if hitboxID != -1:
        for e in effectStringDict:
            currlist = effectStringDict[e]
            if hitboxID == currlist[0] and currlist[1] == 0:
                addEffect(terminateGraphic13)
                markAllHitboxesDeleted()
                break
    effectLines = effectLines + "\t\t"
    tabs = inCompare
    if inLoop:
        tabs = tabs + 1
    for q in range(tabs):
        effectLines = effectLines + "    "
    effectLines = effectLines + effectString + "\r\n"
    effectStringDict[effectString] = [hitboxID, 0]

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
            print(i, end="\n")
        else:
            if i == "\t}\n\r":
                inEffect = False

def getDamageRGB(damageStr, angleStr):
    damage = float(damageStr)
    angle = int(angleStr, 16)
    if 240 <= angle <= 300:
        red = getHexFloat(254)
        green = getHexFloat(0)
        blue = getHexFloat(254)
    elif damage == 0:
        red = getHexFloat(255)
        green = getHexFloat(255)
        blue = getHexFloat(255)
    elif damage > 15:
        red = getHexFloat(254)
        green = getHexFloat(0)
        blue = getHexFloat(0)
    else:
        red = getHexFloat(254)
        green = getHexFloat(254 - (damage * 254 / 15))
        blue = getHexFloat(0)

    return red, green, blue

def addDodgeEffects2(dodgeActive):
    addEffect(asynchronousTimer.format(dodgeActive[0]))
    addEffect(colorOverlay.format("0", "0", "255", "128"))
    addEffect(asynchronousTimer.format(str(int(dodgeActive[1]) + 1)))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def addDodgeEffects(dodgeActive, dodgeFAF):
    # starting frames
    addEffect(colorOverlay.format("0", "255", "0", "128"))
    # invuln
    addEffect(asynchronousTimer.format(dodgeActive[0]))
    addEffect(terminateOverlays)
    addEffect(colorOverlay.format("0", "0", "255", "128"))
    addEffect(asynchronousTimer.format(str(int(dodgeActive[1]) + 1)))
    addEffect(terminateOverlays)
    # lag
    addEffect(colorOverlay.format("0", "255", "0", "128"))
    addEffect(asynchronousTimer.format(dodgeFAF))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def addLagEffects(lagLength):
    addEffect(asynchronousTimer.format("1"))
    addEffect(colorOverlay.format("0", "255", "0", "128"))
    addEffect(asynchronousTimer.format(str(int(lagLength) + 1)))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def main():
    if len(sys.argv) != 2:
        print("Needs one argument: .acm move file path")
        exit()
    filename = sys.argv[1]

    with open(filename, newline="\r\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    global effectLines, inLoop, inCompare
    inMain = False
    shouldExitLoop = False
    gotoNum = 0
    offsetBegin = 0
    offsetEnd = 0
    prevFrame = 0
    condIndex = 0

    tsvLines = []

    # tsvData found in TSV folder; read any file for example layout
    charName = os.path.split(os.path.dirname(filename))[0][:-5]
    if charName[-4:] == "body":
        charName = charName[:-4]
        tsvPath = "TSV/{}.tsv".format(charName)
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
    elif basename == ledgecatch:
        addLagEffects('2')
    elif basename == groundedfootstoolPose:
        addLagEffects('8')
    elif basename == groundedfootstoolBack:
        addLagEffects('20')
    elif basename == spinningAnim:
        addEffect(asynchronousTimer.format('1'))
        addEffect(colorOverlay.format(255, 165, 0, 128))
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
        addEffect(colorOverlay.format("0", "255", "0", "128"))
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

                compare = "If_Compare"
                compare2 = "If_Compare2"
                if i[:len(compare2)] == compare2:
                    addEffect(ifCompare2.format(paramList[0], paramList[1], paramList[2]))
                elif i[:len(compare)] == compare:
                    addEffect(ifCompare.format(paramList[0], paramList[1], paramList[2]))
                ifBitIsSetStr = "If_Bit_is_Set"
                if i[:len(ifBitIsSetStr)] == ifBitIsSetStr:
                    addEffect(ifBitIsSet.format(paramList[0]))
                someCompareStr = "unk_477705C2"
                if i[:len(someCompareStr)] == someCompareStr:
                    addEffect(someCompare.format(paramList[0], paramList[1], paramList[2]))
                someCompareStr2 = "unk_2DA7E2B6"
                if i[:len(someCompareStr2)] == someCompareStr2:
                    addEffect(someCompare2.format(paramList[0], paramList[1], paramList[2]))

                TRUEstr = "TRUE"
                if i[:len(TRUEstr)] == TRUEstr:
                    parseForConditionals(lines)
                    currVar = ""
                    if condIndex < len(condList):
                        currVar = condList[condIndex]
                    else:
                        currVar = paramList[0]
                    addEffect(TRUEComp.format(currVar))
                    condIndex = condIndex + 1
                    inCompare = inCompare + 1

                FALSEstr = "FALSE"
                if i[:len(FALSEstr)] == FALSEstr:
                    parseForConditionals(lines)
                    currVar = ""
                    if condIndex < len(condList):
                        currVar = condList[condIndex]
                    else:
                        currVar = paramList[0]
                    addEffect(FALSEComp.format(currVar))
                    condIndex = condIndex + 1
                    inCompare = inCompare + 1

                gotoStr = "Goto"
                if i[:len(gotoStr)] == gotoStr:
                    addEffect(goto.format(-gotoNum))
                    gotoNum = 0

                loop = "Set_Loop"
                if i[:len(loop)] == loop:
                    loopNum = int(paramList[0])
                    addEffect(setLoop.format(loopNum))
                    inLoop = True

                looprest = "Loop_Rest()"
                if i[:len(looprest)] == looprest:
                    addEffect(looprest)

                armor = "Set_Armor"
                if i[:len(armor)] == armor:
                    state = paramList[0]
                    if state == "0x0":
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(255, 0, 255, 128))

                bodycoll = "Body_Collision"
                if i[:len(bodycoll)] == bodycoll:
                    state = paramList[0]
                    if state == "0x0":
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(0, 0, 255, 128))

                detect = "Search_Collision"
                if i[:len(detect)] == detect:
                    bone = paramList[2]
                    size = getHexFloat(float(paramList[3]) * 19 / 200)
                    z = getHexFloat(float(paramList[4]))
                    y = getHexFloat(float(paramList[5]))
                    x = getHexFloat(float(paramList[6]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255)
                    addEffectID(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue), paramList[0])

                grabcoll2 = "Grab_Collision2"
                if i[:len(grabcoll2)] == grabcoll2:
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255)
                    addEffectID(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue), paramList[0])

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
                    addEffect(colorOverlay.format('255', '0', '0', '128'))

                bitvarset = "Bit_Variable_Set"
                if i[:len(bitvarset)] == bitvarset:
                    var = paramList[0]
                    specialLw = "SpecialLw"
                    if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                        addEffect(colorOverlay.format('255', '0', '0', '128'))

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
                if i[:len(asyncTimer)] == asyncTimer:
                    if offsetEnd != 0:
                        addEffect(asynchronousTimer.format(offsetEnd + prevFrame))
                        addEffect(terminateGraphic13)
                        addEffect(asynchronousTimer.format(offsetBegin + int(paramList[0])))
                        prevFrame = int(paramList[0])
                    else:
                        addEffect(asynchronousTimer.format(paramList[0]))

                syncTimer = "Synchronous_Timer"
                if i[:len(syncTimer)] == syncTimer:
                    addEffect(synchronousTimer.format(paramList[0]))

                undoBone = "Undo_Bone_Collision"
                if i[:len(undoBone)] == undoBone:
                    addEffect(terminateGraphic31)

                removeHitb = "Remove_All_Hitboxes"
                terminateGrab = "Terminate_Grab_Collisions"
                enableAction = "Enable Action Status"
                if i[:len(removeHitb)] == removeHitb or i[:len(terminateGrab)] == terminateGrab or i[:len(enableAction)] == enableAction:
                    addEffect(terminateGraphic13)
                    markAllHitboxesDeleted()

                boneIntangability = "Set_Bone_Intangability"
                if i[:len(boneIntangability)] == boneIntangability:
                    bone = paramList[0]
                    addEffect(setBoneIntangability.format(bone))

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
                    addEffectID(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue), paramList[0])

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
                            addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), paramList[0])
                        else:
                            addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), -1)

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
                            addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), paramList[0])
                        else:
                            addEffectID(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue), -1)

                grabcoll = "Grab_Collision"
                if i[:len(grabcoll)] == grabcoll:
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    addEffectID(grabHitbox.format(bone, z, y, x, size), paramList[0])

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
                            addEffectID(grabHitbox.format(bone, zcurr, ycurr, xcurr, size), paramList[0])
                        else:
                            addEffectID(grabHitbox.format(bone, zcurr, ycurr, xcurr, size), -1)

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

    printOutput(lines)

main()

import sys, struct, os.path

#KuroganeHammer data
gameChars = "bayonetta,captain,cloud,dedede,diddy,donkey,duckhunt,falco,fox,gamewatch,ganon,gekkouga,ike,kamui,kirby,koopa,koopajr,link,littlemac,lizardon,lucario,lucas,lucina,luigi,mario,mariod,marth,metaknight,mewtwo,murabito,ness,pacman,palutena,peach,pikachu,pikmin,pit,pitb,purin,reflet,robot,rockman,rosetta,roy,ryu,samus,sheik,shulk,sonic,szerosuit,toonlink,wario,wiifit,yoshi,zelda".split(",")
kuroChars = "Bayonetta,Captain%20Falcon,Cloud,King%20Dedede,Diddy%20Kong,Donkey%20Kong,Duck%20Hunt,Falco,Fox,Game%20And%20Watch,Ganondorf,Greninja,Ike,Corrin,Kirby,Bowser,Bowser%20Jr,Link,Little%20Mac,Charizard,Lucario,Lucas,Lucina,Luigi,Mario,Dr.%20Mario,Marth,Meta%20Knight,Mewtwo,Villager,Ness,PAC-MAN,Palutena,Peach,Pikachu,Olimar,Pit,Dark%20Pit,Jigglypuff,Robin,R.O.B,Mega%20Man,Rosalina%20And%20Luma,Roy,Ryu,Samus,Sheik,Shulk,Sonic,Zero%20Suit%20Samus,Toon%20Link,Wario,Wii%20Fit%20Trainer,Yoshi,Zelda".split(",")

#game code lines
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

effectLines = "\tEffect()\n\t{\r\n"

spotdodgeActive = []
spotdodgeFAF = ""
frollActive = []
frollFAF = ""
brollActive = []
brollFAF = ""
airdodgeActive = []
airdodgeFAF = ""
ledgejumpActive=[]
ledgejumpFAF=""
ledgerollActive=[]
ledgerollFAF=""
ledgegetupActive=[]
ledgegetupFAF=""
ledgeattackActive=[]
ledgeattackFAF=""

inLoop = False
inCompare = 0
#loopLines = []

def float_to_hex(f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def getHexFloat(value):
        hexFloat = str(float_to_hex(value)).upper()
        return ("".join(c.lower() if (c == "X") else c for i, c in enumerate(hexFloat)))

def getParamList(line):
    parameters = line[line.find("(")+1:line.find(")")]
    fullParamList = parameters.split(',')
    paramList = [x[x.find("=")+1:] for x in fullParamList]
    return paramList

def addEffect(effectString):
    global effectLines#,loopLines
    '''
    if (inCompare):
        effectLines = effectLines + "\t\t    " + effectString + "\r\n"
        #loopLines.append(effectString)
    else:
        effectLines = effectLines + "\t\t" + effectString + "\r\n"
    effectLines = effectLines + "\t\t"
    '''
    effectLines = effectLines + "\t\t"
    for q in range(inCompare):
        effectLines = effectLines + "    "
    effectLines = effectLines + effectString + "\r\n"

def getLastEffectString():
    allEffectLines = effectLines.split("\r\n")
    str = removeBeginningWhitespace(allEffectLines[-2:-1])[0]
    return str

def removeBeginningWhitespace(string):
    removed = ""
    for q in range(len(string)):
            if (string[q].isspace() == False):
                    removed = string[q:]
                    break
    return removed

def removeLastEffect(effectString):
    global effectLines
    str = "\t\t" + effectString + "\r\n"
    effectLines = effectLines[:-len(str)]

def printOutput(lines):
    inEffect = False
    firstLine = True
    for i in lines:
            if (i == "\tEffect()\n\t{\r"):
                    inEffect = True
                    print(effectLines, end="\t}\n\r\n")
            if (inEffect == False):
                    print(i,end="\n")
            else:
                    if (i == "\t}\n\r"):
                          inEffect = False
            firstLine = False

def getDamageRGB(damageStr, angleStr):
    damage = float(damageStr)
    angle = int(angleStr, 16)
    if (angle >= 240 and angle <= 300):
        red = getHexFloat(255)
        green = getHexFloat(0)
        blue = getHexFloat(255)
    elif (damage == 0):
        red = getHexFloat(255)
        green = getHexFloat(255)
        blue = getHexFloat(255)
    elif (damage > 15):
        red = getHexFloat(255)
        green = getHexFloat(0)
        blue = getHexFloat(0)    
    else:
        red = getHexFloat(255)
        green = getHexFloat(255 - (damage * 255 / 15))
        blue = getHexFloat(0)
                    
    return red, green, blue

def addDodgeEffects(dodgeActive):
    addEffect(asynchronousTimer.format(dodgeActive[0]))
    addEffect(colorOverlay.format("0", "0", "255", "128"))
    addEffect(asynchronousTimer.format(str(int(dodgeActive[1])+1)))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)

def addLagEffects(lagLength):
    addEffect(asynchronousTimer.format("1"))
    addEffect(colorOverlay.format("0", "255", "0", "128"))
    addEffect(asynchronousTimer.format(str((int)(lagLength)+1)))
    addEffect(terminateOverlays)
    addEffect(scriptEnd)
	
    
def main():
    if (len(sys.argv) != 2):
        print("Needs one argument: .acm move file path")
        exit()
    filename = sys.argv[1]
    

    with open(filename, newline="\r\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    global effectLines#, loopLines
    inMain = False
    shouldExitLoop = False
    countLoopLines = False
    global inLoop, inCompare
    gotoNum = 0
    loopNum = 0
    loopLines = 0
    offsetBegin = 0
    offsetEnd = 0
    prevFrame = 0

    ## dodgeData
    charName = os.path.split(os.path.dirname(filename))[0][:-5]
    if (charName[-4:] == "body"):
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
    
    if (basename == spotdodge):
        spotdodgeActive = tsvLines[0].split("\t")[0:2]
        addDodgeEffects(spotdodgeActive)
    elif (basename == froll):
        frollActive = tsvLines[2].split("\t")[0:2]
        addDodgeEffects(frollActive)
    elif (basename == broll):
        brollActive = tsvLines[4].split("\t")[0:2]
        addDodgeEffects(brollActive)
    elif (basename == airdodge):
        airdodgeActive = tsvLines[6].split("\t")[0:2]
        addDodgeEffects(airdodgeActive)
    elif (basename == ledgecatch):
        addLagEffects('2')
    elif (basename == groundedfootstoolPose):
        addLagEffects('8')
    elif (basename == groundedfootstoolBack):
        addLagEffects('20')
    elif (basename == spinningAnim):
        addEffect(asynchronousTimer.format('1'))
        addEffect(colorOverlay.format(255, 165, 0, 128))
        addEffect(scriptEnd)
    elif (basename == ledgegetup):
        ledgegetupActive = tsvLines[12].split("\t")[0:2]
        addDodgeEffects(ledgegetupActive)
    elif (basename == ledgeroll):
        ledgerollActive = tsvLines[10].split("\t")[0:2]
        addDodgeEffects(ledgerollActive)
    elif (basename == ledgejump):
        #charName = filename[:-len(ledgejump)-len("Input/animcmd/")]
        #if (charName[-4:] == "body"):
        #    charName = charName[:-4]
        #getLedgeData("ledgejump", charName)
        ledgejumpActive = tsvLines[8].split("\t")[0:2]    
        addDodgeEffects(ledgejumpActive)
    elif (basename == jumpsquat):
        addLagEffects(tsvLines[16].split("\t")[0])
    elif (basename == lightLanding):
        addLagEffects(tsvLines[17].split("\t")[0])
    elif (basename == hardLanding):
        addLagEffects(tsvLines[18].split("\t")[0])
    elif (basename == landingAirN):
        addLagEffects(tsvLines[19].split("\t")[0])
    elif (basename == landingAirF):
        addLagEffects(tsvLines[20].split("\t")[0])
    elif (basename == landingAirB):
        addLagEffects(tsvLines[21].split("\t")[0])
    elif (basename == landingAirHi):
        addLagEffects(tsvLines[22].split("\t")[0])
    elif (basename == landingAirLw):
        addLagEffects(tsvLines[23].split("\t")[0])
    elif (basename in {passive, passiveF, passiveB}):
        addDodgeEffects(['1', '20'])
    elif (basename == downStandU): 
          addDodgeEffects(tsvLines[25].split("\t")[0:2])
    elif (basename == downStandD): 
          addDodgeEffects(tsvLines[27].split("\t")[0:2])
    elif (basename == downForwardU): 
          addDodgeEffects(tsvLines[29].split("\t")[0:2])
    elif (basename == downForwardD): 
          addDodgeEffects(tsvLines[31].split("\t")[0:2])
    elif (basename == downBackU): 
          addDodgeEffects(tsvLines[33].split("\t")[0:2])
    elif (basename == downBackD): 
          addDodgeEffects(tsvLines[35].split("\t")[0:2])
    elif (basename in {downBoundU, downBoundD}):
          addEffect(downEffect1)
          addEffect(downEffect2)
          addEffect(scriptEnd)
    else:
        if (basename == ledgeattack):
            ledgeattackActive = tsvLines[14].split("\t")[0:2]
            addDodgeEffects(ledgeattackActive)
            removeLastEffect(scriptEnd)
        index = 0
        while (index < len(lines)):
            iorig = lines[index]
            i = ''
            #EXPERIMENTAL
            for q in range(len(iorig)):
                if (iorig[q].isspace() == False):
                    i = iorig[q:]
                    break
            #print(i, index)
            
            if (i == "Main()\n\t{\r"):
                inMain = True
                if (lines[index+1] == "\t}\n\r"):
                        break
            if (shouldExitLoop):
                break
            if (inMain):
                paramList = getParamList(i)
                #print(paramList[0], i)
                endlooporcompare = "}"
                if (i[:len(endlooporcompare)] == endlooporcompare):
                    if (inCompare):
                        inCompare = inCompare - 1
                        addEffect(endLoopOrCompare)
                    inLoop = False

                compare = "If_Compare"    
                compare2 = "If_Compare2"
                if (i[:len(compare2)] == compare2):
                    addEffect(ifCompare2.format(paramList[0], paramList[1], paramList[2]))    
                elif (i[:len(compare)] == compare):
                    addEffect(ifCompare.format(paramList[0], paramList[1], paramList[2]))
                ifBitIsSetStr = "If_Bit_is_Set"
                if (i[:len(ifBitIsSetStr)] == ifBitIsSetStr):
                    addEffect(ifBitIsSet.format(paramList[0]))
                someCompareStr = "unk_477705C2"
                if (i[:len(someCompareStr)] == someCompareStr):
                    addEffect(someCompare.format(paramList[0], paramList[1], paramList[2]))
                someCompareStr2 = "unk_2DA7E2B6"
                if (i[:len(someCompareStr2)] == someCompareStr2):
                    addEffect(someCompare2.format(paramList[0], paramList[1], paramList[2]))

                TRUEstr = "TRUE"
                if (i[:len(TRUEstr)] == TRUEstr):
                    val = hex(int(paramList[0], 16) - 118)
                    addEffect(TRUEComp.format(paramList[0]))
                    inCompare = inCompare + 1

                FALSEstr = "FALSE"
                if (i[:len(FALSEstr)] == FALSEstr):
                    val = hex(int(paramList[0], 16) - 118)
                    addEffect(FALSEComp.format(paramList[0]))
                    inCompare = inCompare + 1

                if (inLoop or inCompare):
                    #i = i[0:2] + i[6:]
                    gotoNum = gotoNum + len(paramList)

                #gotoStr = "\t\tGoto"
                #if (i[:len(gotoStr)] == gotoStr):
                    #loopLineParamLength = 0
                    #for l in loopLines:
                    #    loopLineParamLength = loopLineParamLength + len(getParamList(l))
                    #loopLines = []
                    #addEffect(goto.format(-loopLineParamLength-5))

                loop = "Set_Loop"
                if (i[:len(loop)] == loop):
                        loopNum = int(paramList[0])
                        if (loopNum < 0):
                                loopNum = 0
                        loopLines = 0
                        countLoopLines = True
                        
                endloop1 = "}"
                endloop2 = "}"
                if (i[:len(endloop1)] == endloop1 or i[:len(endloop2)] == endloop2):
                        if (loopNum != 0):
                                index = index - loopLines
                                loopNum = loopNum - 1
                                inLoop = True
                        else:
                                inLoop = False
                        countLoopLines = False

                #if (loopNum > 0):
                #        i = i[0:2] + i[6:]
                if (countLoopLines):
                    loopLines = loopLines + 1

                armor = "Set_Armor"
                if (i[:len(armor)] == armor):
                    state = paramList[0]
                    if (state == "0x0"):
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(255, 0, 255, 128))

                bodycoll = "Body_Collision"
                if (i[:len(bodycoll)] == bodycoll):
                    state = paramList[0]
                    if (state == "0x0"):
                        addEffect(terminateOverlays)
                    else:
                        addEffect(colorOverlay.format(0, 0, 255, 128))
                
                detect = "Search_Collision"
                if (i[:len(detect)] == detect):
                    bone = paramList[2]
                    size = getHexFloat(float(paramList[3]) * 19 / 200)
                    z = getHexFloat(float(paramList[4])) 
                    y = getHexFloat(float(paramList[5])) 
                    x = getHexFloat(float(paramList[6]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255)
                    addEffect(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue))

                grabcoll2 = "Grab_Collision2"
                if (i[:len(grabcoll2)] == grabcoll2):
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    z = getHexFloat(float(paramList[3])) 
                    y = getHexFloat(float(paramList[4])) 
                    x = getHexFloat(float(paramList[5]))
                    red, green, blue = getHexFloat(0), getHexFloat(255), getHexFloat(255) 
                    addEffect(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue))

                subr = "Subroutine"
                if (i[:len(subr)] == subr):
                    hash = paramList[0]
                    if (basename != "Attack100.acm"):
                        addEffect(subroutine.format(hash))

                extsubr = "External_Subroutine"
                if (i[:len(extsubr)] == extsubr):
                    hash = paramList[0]
                    if (basename != "Attack100.acm"):
                        addEffect(extsubroutine.format(hash))

                defensive = "Defensive_Collision"
                if (i[:len(defensive)] == defensive):
                    addEffect(colorOverlay.format('255', '0', '0', '128'))

                bitvarset = "Bit_Variable_Set"
                if (i[:len(bitvarset)] == bitvarset):
                    var = paramList[0]
                    if (var == "0x2100000E"): #counter
                        addEffect(colorOverlay.format('255', '0', '0', '128'))
                    '''
                    if (var == "0x2100000D"): 
                        addEffect(bitVariableSet.format(paramList[0]))
                    if (var == "0x21000014"): 
                        addEffect(bitVariableSet.format(paramList[0]))
                    if (var == "0x21000000"):
                        addEffect(bitVariableSet.format(paramList[0]))
                    '''    

                bitvarclear = "Bit_Variable_Clear"
                if (i[:len(bitvarset)] == bitvarset):
                    var = paramList[0]
                    if (var == "0x2100000E"):
                        addEffect(terminateOverlays)

                terminateDefensive = "Terminate_Defensive_Collision"
                if (i[:len(terminateDefensive)] == terminateDefensive):
                    addEffect(terminateOverlays)

                basicvarset = "Basic_Variable_Set"
                if (i[:len(basicvarset)] == basicvarset):
                    if (offsetBegin == 0 and paramList[1] == "0x1100000F"):
                        offsetBegin = int(paramList[0], 16)
                        prevFrame = int(getParamList(getLastEffectString())[0])
                        removeLastEffect(asynchronousTimer.format(prevFrame)) 
                        addEffect(asynchronousTimer.format(prevFrame + offsetBegin))
                    elif (paramList[1] == "0x11000010"):
                        offsetEnd = int(paramList[0], 16)
                asyncTimer = "Asynchronous_Timer"
                if (i[:len(asyncTimer)] == asyncTimer):
                    if (offsetEnd != 0):
                        addEffect(asynchronousTimer.format(offsetEnd + prevFrame))
                        addEffect(terminateGraphic13)
                        addEffect(asynchronousTimer.format(offsetBegin + (int)(paramList[0])))
                        prevFrame = (int)(paramList[0])
                    else:
                        addEffect(asynchronousTimer.format(paramList[0]))
                        
                syncTimer = "Synchronous_Timer"
                if (i[:len(syncTimer)] == syncTimer):
                    addEffect(synchronousTimer.format(paramList[0]))
                
                undoBone = "Undo_Bone_Collision"
                if (i[:len(undoBone)] == undoBone):
                    addEffect(terminateGraphic31)

                removeHitb = "Remove_All_Hitboxes"
                terminateGrab = "Terminate_Grab_Collisions"
                enableAction = "Enable Action Status"
                if (i[:len(removeHitb)] == removeHitb or i[:len(terminateGrab)] == terminateGrab or i[:len(enableAction)] == enableAction):
                    addEffect(terminateGraphic13)
                    
                boneIntangability = "Set_Bone_Intangability"
                if (i[:len(boneIntangability)] == boneIntangability):
                    bone = paramList[0]
                    addEffect(setBoneIntangability.format(bone))
                                
                hitb = "Hitbox"
                specialHitb = "Special_Hitbox"
                if (i[:len(hitb)] == hitb or i[:len(specialHitb)] == specialHitb):
                    bone = paramList[2]
                    size = getHexFloat(float(paramList[8]) * 19 / 200)
                    z = getHexFloat(float(paramList[9])) 
                    y = getHexFloat(float(paramList[10])) 
                    x = getHexFloat(float(paramList[11]))
                    red, green, blue = getDamageRGB(paramList[3], paramList[4])
                    #addEffect(normalOrSpecialHitbox.format(bone, z, y, x, size))
                    addEffect(normalOrSpecialHitboxNew.format(bone, z, y, x, size, red, green, blue))
                
                extendedHitb = "Extended_Hitbox"
                if (i[:len(extendedHitb)] == extendedHitb):
                    bone = paramList[2]
                    size = getHexFloat(float(paramList[8]) * 19 / 200)
                    zinit = float(paramList[9])
                    yinit = float(paramList[10])
                    xinit = float(paramList[11])
                    zfinal = float(paramList[24])
                    yfinal = float(paramList[25])
                    xfinal = float(paramList[26])
                    for j in range(0,4):
                        #PUT CONDITIONS?! All 6?
                        zcurr = getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
                        ycurr = getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
                        xcurr = getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
                        red, green, blue = getDamageRGB(paramList[3], paramList[4])
                        #addEffect(extendedHitbox.format(bone, zcurr, ycurr, xcurr, size))
                        addEffect(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue))

                extendedSpecialHitb = "Extended_Special_Hitbox"
                if (i[:len(extendedSpecialHitb)] == extendedSpecialHitb):
                        bone = paramList[2]
                        size = getHexFloat(float(paramList[8]) * 19 / 200)
                        zinit = float(paramList[9])
                        yinit = float(paramList[10])
                        xinit = float(paramList[11])
                        zfinal = float(paramList[40])
                        yfinal = float(paramList[41])
                        xfinal = float(paramList[42])
                        for j in range(0,8):
                                #PUT CONDITIONS?! All 6?
                                zcurr = getHexFloat(zinit + ((zfinal - zinit) / 7 * j))
                                ycurr = getHexFloat(yinit + ((yfinal - yinit) / 7 * j))
                                xcurr = getHexFloat(xinit + ((xfinal - xinit) / 7 * j))
                                red, green, blue = getDamageRGB(paramList[3], paramList[4])
                                #addEffect(extendedHitbox.format(bone, zcurr, ycurr, xcurr, size))
                                addEffect(extendedHitboxNew.format(bone, zcurr, ycurr, xcurr, size, red, green, blue))

                grabcoll = "Grab_Collision"
                if (i[:len(grabcoll)] == grabcoll):
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2])*19/200)
                    z = getHexFloat(float(paramList[3]))
                    y = getHexFloat(float(paramList[4]))
                    x = getHexFloat(float(paramList[5]))
                    addEffect(grabHitbox.format(bone, z, y, x, size))
                    
                grabHitb = "Extended_Grab_Collision"
                if (i[:len(grabHitb)] == grabHitb):
                    bone = paramList[1]
                    size = getHexFloat(float(paramList[2]) * 19 / 200)
                    zinit = float(paramList[3])
                    yinit = float(paramList[4])
                    xinit = float(paramList[5])
                    zfinal = zinit #float(paramList[8]) #zinit??
                    yfinal = float(paramList[9])
                    xfinal = float(paramList[10])
                    for j in range(0,3):
                        #PUT CONDITIONS?! All 6?
                        zcurr = getHexFloat(zinit + ((zfinal - zinit) / 2 * j))
                        ycurr = getHexFloat(yinit + ((yfinal - yinit) / 2 * j))
                        xcurr = getHexFloat(xinit + ((xfinal - xinit) / 2 * j))
                        addEffect(grabHitbox.format(bone, zcurr, ycurr, xcurr, size))
            
                scriptFin = "Script_End()"
                if (i[:len(scriptFin)] == scriptFin):
                    if (offsetBegin != 0):
                        addEffect(asynchronousTimer.format(prevFrame + offsetEnd))
                        addEffect(terminateGraphic13)
                    addEffect(scriptEnd)
                    inMain = False
                    shouldExitLoop = True
            index = index + 1

    printOutput(lines)
                          
main()

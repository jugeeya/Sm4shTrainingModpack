import os, struct, math
from collections import OrderedDict

gameChars = "bayonetta,captain,cloud,dedede,diddy,donkey,duckhunt,falco,fox,gamewatch,ganon,gekkouga,ike,kamui,kirby,koopa,koopajr,link,littlemac,lizardon,lucario,lucas,lucina,luigi,mario,mariod,marth,metaknight,mewtwo,murabito,ness,pacman,palutena,peach,pikachu,pikmin,pit,pitb,purin,reflet,robot,rockman,rosetta,roy,ryu,samus,sheik,shulk,sonic,szerosuit,toonlink,wario,wiifit,yoshi,zelda,miiswordsman,miifighter,miigunner".split(",")
counterChars = "gekkouga,ike,kamui,littlemac,lucario,lucina,marth,palutena,peach,roy,shulk".split(",")

# game code lines
asynchronousTimer = "Asynchronous_Timer(Frames={})"
synchronousTimer = "Synchronous_Timer(Frames={})"
setBoneIntangability = "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)"
setHurtbox = "Graphic_Effect6(Graphic=0x1000031, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
setHurtboxIntang = "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)"
setHurtboxTest = "Graphic_Effect6(Graphic={}, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
showAngle = "Graphic_Effect6(Graphic=0x1000094, Bone=0x0, Z={}, Y={}, X={}, ZRot={}, YRot=0, XRot=0, Size=0.5, Terminate=0x1, Unknown=0x420C0000)"
showSegmentGreen = "Graphic_Effect6(Graphic=0x1000057, Bone=0x0, Z={}, Y={}, X={}, ZRot={}, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
# z,y,x,zrot,size
showSegment = "EFFECT_FOLLOW_COLOR(unknown=0x1000057, unknown=0x0, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown={}, unknown={}, unknown={})"
grayHitbox = "Graphic_Effect6(Graphic=0x1000013, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
coloredHitbox = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown={}, unknown={}, unknown={})"
grabHitbox = "EFFECT_FOLLOW_COLOR(unknown=0x1000013, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown=0x0, unknown=0x437F0000, unknown=0x0)"
terminateGraphic13 = "Terminate_Graphic_Effect(Graphic=0x1000013, unknown=0x1, unknown=0x1)"
terminateGraphic31 = "Terminate_Graphic_Effect(Graphic=0x1000031, unknown=0x1, unknown=0x1)"
terminateGraphic57 = "Terminate_Graphic_Effect(Graphic=0x1000057, unknown=0x1, unknown=0x1)"
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
allowInterrupt = "Allow_Interrupt()"
scriptEnd = "Script_End()"

# colors: R, G, B, Alpha
ALPHA = '128'

PINK = ['255', '105', '180', ALPHA]
RED = ['255', '0', '0', ALPHA]
ORANGE = ['255', '165', '0', ALPHA]
YELLOW = ['255', '255', '0', ALPHA]
GREEN = ['0', '255', '0', ALPHA]
BLUE = ['0', '0', '255', ALPHA]
PURPLE = ['85', '26', '139', ALPHA]
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
canReallyAirdodgeVar = "0x2000232" # orig 0.5
canReallyAnyActionVar = "0x2000233" # orig 0.84
shieldDegenVar = "0x20000C7"
shieldRegenVar = "0x20000C8"
shieldDamageMultVar = "0x20000CA"
noBufferVar = "0x2000218"
ledgeWaitFrameVar = "0x2000230" # super mushroom size multiplier? orig 1.7
ourLaunchSpeedVar = "0x2000231" # related to super mushroom. orig 0.5
hitstunVar = "0x1000003E"
launchSpeedVar = "0x10000003" # launch speed basic
currentPercentVar = "0x11000010"
shouldShieldVar = "0x2000234" # poison mushroom voice pitch mult, orig 1.25
playerNumVar = "0x100000AC"
playerOneVar = "0x200000A5"
extraVar = "0x21000027" # some other ryu thing

# alphabet: char : segmentList [segmentAttrList [Z, Y, X, ZRot, (optional isHalf=1)] ...]
# sevSeg :
#       _
#      |_| from top to top left, clockwise: a->f + g mid +  \|/ from top mid to top left, clockwise: h->m + --two half g's: n, o
#      |_|                                                  /|\
#
raygunLength = 8
raygunHeight = 6
raygunHorizOffset = 2
segmentDict = {
    'a': [0,raygunHeight*2,raygunLength/2+raygunHorizOffset+1,0],
    'b': [0,raygunHeight,raygunLength,90],
    'c': [0,0,raygunLength,90],
    'd': [0,0,raygunLength/2+raygunHorizOffset+1,0],
    'e': [0,0,0,90],
    'f': [0,raygunHeight,0,90],
    'g': [0,raygunHeight,raygunLength/2+raygunHorizOffset+1,0],
    'h': [0,raygunHeight,raygunLength/2,90],
    'i': [0,raygunHeight*2,raygunLength/2+2*raygunHorizOffset,-52,0.45],
    'j': [0,0,raygunLength/2+2*raygunHorizOffset,52,0.45],
    'k': [0,0,raygunLength/2,90],
    'l': [0,raygunHeight,raygunLength/2,-52,0.45],
    'm': [0,raygunHeight,raygunLength/2,52,0.45],
    'n': [0,raygunHeight,raygunHorizOffset+1,0,0.25],
    'o': [0,raygunHeight,raygunLength/2+raygunHorizOffset+1,0,0.25],
}

alphabet = {
    'A': [segmentDict[x] for x in ['a','b','c','e','f','g']],
    'B': [segmentDict[x] for x in ['a','d','e','f','i','j','n']],
    'C': [segmentDict[x] for x in ['a','d','e','f']],
    'D': [segmentDict[x] for x in ['e','f','l','m']],
    'E': [segmentDict[x] for x in ['a','d','e','f','n']],
    'F': [segmentDict[x] for x in ['a','e','f','n']],
    'G': [segmentDict[x] for x in ['a','c','d','e','f','o']],
    'H': [segmentDict[x] for x in ['b','c','e','f','g']],
    'I': [segmentDict[x] for x in ['a','d','h','k']],
    'J': [segmentDict[x] for x in ['b','c','d']],
    'K': [segmentDict[x] for x in ['e','f','n','i','j']],
    'L': [segmentDict[x] for x in ['d','e','f']],
    'M': [segmentDict[x] for x in ['b','c','e','f','i','m']],
    'N': [segmentDict[x] for x in ['b','c','e','f','j','m']],
    'O': [segmentDict[x] for x in ['a','b','c','d','e','f']],
    'P': [segmentDict[x] for x in ['a','b','e','f','g']],
    'Q': [segmentDict[x] for x in ['a','b','c','d','e','f','j']],
    'R': [segmentDict[x] for x in ['a','e','f','i','j','n']],
    'S': [segmentDict[x] for x in ['a','c','d','f','g']],
    'T': [segmentDict[x] for x in ['a','h','k']],
    'U': [segmentDict[x] for x in ['b','c','d','e','f']],
    'V': [segmentDict[x] for x in ['e','f','i','l']],
    'W': [segmentDict[x] for x in ['b','c','e','f','j','l']],
    'X': [segmentDict[x] for x in ['i','j','l','m']],
    'Y': [segmentDict[x] for x in ['i','k','m']],
    'Z': [segmentDict[x] for x in ['a','d','i','l']],
    '0': [segmentDict[x] for x in ['a','b','c','d','e','f']],
    '1': [segmentDict[x] for x in ['e','f']],
    '2': [segmentDict[x] for x in ['a','b','d','e','g']],
    '3': [segmentDict[x] for x in ['a','b','c','d','g']],
    '4': [segmentDict[x] for x in ['b','c','f','g']],
    '5': [segmentDict[x] for x in ['a','c','d','f','g']],
    '6': [segmentDict[x] for x in ['a','c','d','e','f','g']],
    '7': [segmentDict[x] for x in ['a','b','c']],
    '8': [segmentDict[x] for x in ['a','b','c','d','e','f','g']],
    '9': [segmentDict[x] for x in ['a','b','c','d','f','g']],
    ' ': [],
    '+': [segmentDict[x] for x in ['g','h','k']],
    '#': [segmentDict[x] for x in ['a','b','c','d','e','f','h','i','j','k','l','m','n','o']] # all segments
}
alphabetReversed = {}
segmentReverseDict = {
    'b': 'f',
    'c': 'e',
    'e': 'c',
    'f': 'b',
    'i': 'm',
    'j': 'l',
    'l': 'j',
    'm': 'i',
    'n': 'o',
    'o': 'n',
}
for char in alphabet:
    alphabetReversed[char] = []
    for segment in alphabet[char]:
        shouldContinue = False
        for segName in segmentReverseDict:
            if segment == segmentDict[segName]:
                alphabetReversed[char].append(segmentDict[segmentReverseDict[segName]])
                shouldContinue = True
        if not shouldContinue:
            alphabetReversed[char].append(segment)

shortChars = ['D','1']

class ACMFile:
    def __init__(self, filePath=None, variableLines="", damageLines=""):
        self.filePath = filePath
        self.shouldProcessVariables = False
        self.wifiSafe = False
        self.effectLines = "\tEffect()\n\t{\r\n"
        self.variableEffectLines = variableLines
        self.damageEffectLines = damageLines
        self.mainList = []
        self.myLines = []
        self.origEffectLines = ""
        self.origIndex = 0
        self.blacklisted = False
        self.trainingOnly = False
        self.weaponBool = False
        self.inLoop = False
        self.inCompare = 0
        self.FAF = 10000
        self.invStart = 10000
        self.invEnd = 10000
        # self.hurtboxes: hurtboxNum : attrList [X, ...]
        self.hurtboxes = {}
        self.currentFrame = 0

    def getSpecificEffectLines(self):
        return [self.variableEffectLines, self.damageEffectLines]

    def isInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def printChar(self, charToPrint, lineNum, horizOffset, facingLeft=False, addToString=False):
        if facingLeft:
            segments = alphabetReversed[charToPrint]
        else:
            segments = alphabet[charToPrint]
        lineOffset = 40 - (lineNum * 16)
        savedSegments = []
        for segment in segments:
            z = self.getHexFloat(segment[0])
            y = self.getHexFloat(segment[1] + lineOffset)
            x = self.getHexFloat(segment[2] + horizOffset)
            zrot = self.getHexFloat(segment[3])
            size = self.getHexFloat(0.5)
            if len(segment) == 5:
                size = self.getHexFloat(segment[4])
            hexColor = [self.getHexFloat(int(x)) for x in BLACK][:-1]
            segmentEffect = showSegment.format(z,y,x,zrot,size,*hexColor)
            if not addToString:
                self.addEffect(segmentEffect)
            savedSegments.append(segmentEffect)
        return savedSegments

    def printString(self, stringToPrint, addToString=False):
        lineNum = 0
        horizOffset = 0
        charNum = 0

        facingLeft = True
        savedEffects = []
        savedEffects.append(ifCompare.format("0x0","0x4","0x0"))
        savedEffects.append(TRUEComp.format("0x12"))
        if not addToString:
            self.addEffect(ifCompare.format("0x0","0x4","0x0"))
            self.addEffect(TRUEComp.format("0x12"))
        self.inCompare+=1
        for i in range(0,2):
            lineNum = 0
            if len(stringToPrint) <= 8 and "\n" not in stringToPrint:
                lineNum = 1
            horizOffset = 0
            charNum = 0
            for char in stringToPrint:
                if char == "\n":
                    horizOffset = 0
                    charNum = 0
                    lineNum+=1
                    continue
                effects = self.printChar(char.upper(), lineNum, horizOffset, facingLeft, addToString)
                if addToString:
                    for effect in effects:
                        savedEffects.append(effect)
                charNum+=1
                if char in shortChars:
                    if facingLeft:
                        horizOffset -= (raygunLength/2 + 4)
                    else:
                        horizOffset += (raygunLength/2 + 4)
                else:
                    if facingLeft:
                        horizOffset -= (raygunLength+4)
                    else:
                        horizOffset += (raygunLength+4)

                if charNum > 8:
                    horizOffset = 0
                    charNum = 0
                    lineNum+=1
            if i == 0:
                self.inCompare -= 1
                savedEffects.append("}")
                savedEffects.append(FALSEComp.format("0x10"))
                if not addToString:
                    self.addEffect("}")
                    self.addEffect(FALSEComp.format("0x10"))
                self.inCompare += 1
                facingLeft = False
        self.inCompare -= 1
        savedEffects.append("}")
        if not addToString:
            self.addEffect("}")
        return savedEffects

    def addHitstunOverlays(self, spinning=False):
        if self.damageEffectLines == "":
            self.effectLines = "\tEffect()\n\t{\r\n"
            self.addEffect(basicCompare.format(showFullModVar, greaterThanOrEqualTo, hex(1)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(floatVariableSet.format(0, ourLaunchSpeedVar))
            self.addEffect(floatVariableSet.format(0, canReallyAirdodgeVar))
            self.addEffect(floatVariableSet.format(0, canReallyAnyActionVar))
            self.addEffect(bitVariableClear.format(canAttackVar))
            self.addEffect(bitVariableClear.format(canAirdodgeVar))
            self.addEffect(floatCompare.format(noBufferVar, greaterThanOrEqualTo, self.getHexFloat(19.0)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(floatVariableSet.format(0.8, noBufferVar))
            self.inCompare -= 1
            self.addEffect('}')
            # if facing right? check directions.
            self.addEffect(ifCompare.format("0x0", "0x4", "0x0"))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare+=1
            self.addEffect(floatVariableSet.format(1.0, DIDirectionVar))
            self.inCompare-=1
            self.addEffect("}")
            self.addEffect(FALSEComp.format("0x10"))
            self.inCompare+=1
            self.addEffect(floatVariableSet.format(-1.0, DIDirectionVar))
            self.inCompare-=1
            self.addEffect("}")
            for i in range(1, 150):
                self.addEffect(asynchronousTimer.format(i))

                self.addEffect(ifBitIsSet.format("0x2100000E")) # var game uses when hitstun <= 0
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare+=1;
                self.addEffect(floatVariableSet.format(1, canReallyAnyActionVar))
                self.inCompare-=1;
                self.addEffect("}")

                # 1 tab
                self.addEffect(basicCompare.format(hitstunVar, greaterThanOrEqualTo, hex(1)))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare = self.inCompare + 1
                # 2 tabs
                self.addEffect(floatCompare.format(ourLaunchSpeedVar, equalTo, self.getHexFloat(1)))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                # 3 tabs
                self.addEffect(ifBitIsSet.format(canAttackVar))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                self.addEffect(colorOverlay.format(*MAGENTA))
                self.inCompare -= 1
                self.addEffect("}")
                # 3 tabs
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare += 1
                # 4 tabs
                self.addEffect(ifBitIsSet.format(canAirdodgeVar))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                self.addEffect(colorOverlay.format(*CYAN))
                self.addEffect(floatVariableSet.format(1, canReallyAirdodgeVar))
                self.inCompare -= 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare += 1
                if spinning:
                    self.addEffect(colorOverlay.format(*ORANGE))
                else:
                    self.addEffect(colorOverlay.format(*GREEN))
                self.inCompare -= 1
                self.addEffect("}")
                self.inCompare -= 1
                self.addEffect("}")
                # 2 tabs
                self.inCompare -= 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format('0x10'))
                self.inCompare += 1
                # 3 tabs
                self.addEffect(basicCompare.format(hitstunVar, greaterThanOrEqualTo, hex(40)))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                self.addEffect(floatVariableSet.format(1, ourLaunchSpeedVar))
                self.inCompare -= 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare += 1
                if spinning:
                    self.addEffect(colorOverlay.format(*ORANGE))
                else:
                    self.addEffect(colorOverlay.format(*GREEN))
                self.inCompare -= 1
                self.addEffect("}")
                self.inCompare -= 1
                self.addEffect("}")
                self.inCompare = self.inCompare - 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare = self.inCompare + 1
                self.addEffect(terminateOverlays)
                self.addEffect(floatVariableSet.format(1, canReallyAnyActionVar))
                self.inCompare -= 1
                untilCompare = 2 if not self.wifiSafe else 0
                while self.inCompare > untilCompare:
                    self.addEffect("}")
                    self.inCompare = self.inCompare - 1
                self.addEffect("}")
            self.addEffect(scriptEnd)
            self.damageEffectLines = self.effectLines
        else:
            self.effectLines = self.damageEffectLines

    def parseForEffect(self, lines):
        inEffect = False
        for l in lines:
            if l.startswith("\t}"):
                inEffect = False
            if l.startswith("\tEffect()"):
                inEffect = True
            elif inEffect:
                if not l.startswith("\t\tScript_End()") and not l == "\t\tTRUE(Unknown=0x2)\r":
                    self.origEffectLines = self.origEffectLines + "\t" + l + "\n"

    def moreHitboxesExist(self, remainingLines):
        for i in remainingLines:
            if i.find("Hitbox") != -1 or i.find("Grab") != -1:
                return True
        return False

    def moreTimersExist(self, remainingLines):
        for i in remainingLines:
            if i.find('}') != -1:
                return False
            if i.find("Synchronous_Timer") != -1 or i.find("Asynchronous_Timer") != -1:
                return True
        return False

    def getTSVLine(self, moveName, tsvLines):
        for line in tsvLines:
            for value in line.split("\t"):
                if value[:len(moveName)] == moveName:
                    return line
        return "Not Found"

    def didProcessEndlag(self, lines, index, basename, tsvLines):
        if not self.moreHitboxesExist(lines[index + 1:]):
            currMove = basename[:-4]
            if self.FAF != 10000:
                self.addEffect(colorOverlay.format(*GREEN))
                return True
        #if self.blacklisted:
        #    self.effectLines = "\t\t" + scriptEnd + "\r\n"
        return False

    def addHurtboxes(self):
        for hurtb in self.hurtboxes:
            h = self.hurtboxes[hurtb]
            xinit = float(h[0])
            yinit = float(h[1])
            zinit = float(h[2])
            xfinal = float(h[3])
            yfinal = float(h[4])
            zfinal = float(h[5])
            size = self.getHexFloat(float(h[6])) #* 19 / 200
            bone = hex(int(h[7]))
            for j in range(0, 4):
                zcurr = self.getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
                ycurr = self.getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
                xcurr = self.getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
                self.addEffect(setHurtbox.format(bone, xcurr, ycurr, zcurr, size))

    def addHurtboxIntangibility(self, givenBone):
        for hurtb in self.hurtboxes:
            h = self.hurtboxes[hurtb]
            xinit = float(h[0])
            yinit = float(h[1])
            zinit = float(h[2])
            xfinal = float(h[3])
            yfinal = float(h[4])
            zfinal = float(h[5])
            size = self.getHexFloat(float(h[6])) #* 19 / 200
            size = '0x3FC00000' # default size until I get a better graphic
            bone = hex(int(h[7]))
            if bone == hex(int(givenBone, 16)):
                for j in range(0, 4):
                    zcurr = self.getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
                    ycurr = self.getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
                    xcurr = self.getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
                    self.addEffect(setHurtboxIntang.format(bone, xcurr, ycurr, zcurr, size))

    def floatToHex(self, f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    def getHexFloat(self, value):
        hexFloat = str(self.floatToHex(value)).upper()
        return "".join(c.lower() if (c == "X") else c for i, c in enumerate(hexFloat))

    def getParamList(self, line):
        parameters = line[line.find("(") + 1:line.find(")")]
        fullParamList = parameters.split(',')
        paramList = [x[x.find("=") + 1:] for x in fullParamList]
        return paramList

    def addListToMain(self, index):
        self.origIndex = index
        self.addEffect(terminateGraphic13)
        for h in self.mainList:
            inserted = "\t\t" + h
            index = index + 1
            self.myLines.insert(index, inserted)
        return

    def addToMainList(self, line,index):
        lineFound = False
        for h in self.mainList:
            if h == line:
                lineFound = True
        if self.removeFromMainList(self.getParamList(line)[0]):
            self.mainList.append(line)
            if not lineFound:
                self.addListToMain(index)
        else:
            self.mainList.append(line)

    def addMovedToMainList(self, line,index):
        newLine = ""
        for h in self.mainList:
            if self.getParamList(h)[0] == self.getParamList(line)[0]:
                newLine = h
                self.removeFromMainList(self.getParamList(h)[0])
        boneIndex = newLine.find("Bone=")
        commaIndex = newLine[boneIndex:].find(",")
        newBone = self.getParamList(line)[1]
        newBoneStr = "Bone={}".format(newBone)
        newLine = newLine[:boneIndex] + newBoneStr + newLine[boneIndex+commaIndex:]
        xIndex = newLine.find("X=")
        commaIndex = newLine[xIndex:].find(",")
        newX = float(self.getParamList(line)[2])
        newXStr = "X={}".format(newX)
        newLine = newLine[:xIndex] + newXStr + newLine[xIndex + commaIndex:]
        yIndex = newLine.find("Y=")
        commaIndex = newLine[yIndex:].find(",")
        newY = float(self.getParamList(line)[3])
        newYStr = "Y={}".format(newY)
        newLine = newLine[:yIndex] + newYStr + newLine[yIndex + commaIndex:]
        zIndex = newLine.find("Z=")
        commaIndex = newLine[zIndex:].find(",")
        newZ = float(self.getParamList(line)[4])
        newZStr = "Z={}".format(newZ)
        newLine = newLine[:zIndex] + newZStr + newLine[zIndex + commaIndex:]
        self.mainList.append(newLine)

    def addChangedToMainList(self, line,index):
        newLine = ""
        for h in self.mainList:
            if self.getParamList(h)[0] == self.getParamList(line)[0]:
                newLine = h
                self.removeFromMainList(self.getParamList(h)[0])
        sizeIndex = newLine.find("Size=")
        commaIndex = newLine[sizeIndex:].find(",")
        newSize = float(self.getParamList(line)[1]) # already been processed: * 19 / 200
        newSizeStr = "Size={}".format(newSize)
        newLine = newLine[:sizeIndex] + newSizeStr + newLine[sizeIndex+commaIndex:]
        self.mainList.append(newLine)

    def removeFromMainList(self, hitboxID):
        for h in self.mainList:
            if self.getParamList(h)[0] == hitboxID:
                self.mainList.remove(h)
                return True
        return False

    def addEffect(self, effectString):
        if effectString == scriptEnd and not self.shouldProcessVariables and not self.weaponBool and not self.wifiSafe:
            return
        self.effectLines = self.effectLines + "\t\t"
        tabs = self.inCompare
        if self.inLoop:
            tabs = tabs + 1
        for q in range(tabs):
            self.effectLines = self.effectLines + "    "

        self.effectLines = self.effectLines + effectString + "\r\n"

    def addEffectToString(self, effectString, string):
        if effectString == scriptEnd and not self.shouldProcessVariables and not self.weaponBool and not self.wifiSafe:
            return string
        string = string + "\t\t"
        tabs = self.inCompare
        if self.inLoop:
            tabs = tabs + 1
        for q in range(tabs):
            string = string + "    "

        string = string + effectString + "\r\n"
        return string

    def getLastEffectString(self):
        allEffectLines = self.effectLines.split("\r\n")
        return self.removeBeginningWhitespace(allEffectLines[-2:-1])[0]

    def removeBeginningWhitespace(self, string):
        removed = ""
        for q in range(len(string)):
            if not string[q].isspace():
                removed = string[q:]
                break
        return removed

    def removeLastEffectString(self):
        tabIndex = self.effectLines.rfind("\t")
        while (self.effectLines[tabIndex] == "\t"):
            tabIndex = tabIndex - 1
        self.effectLines = self.effectLines[:tabIndex+1]

    def removeLastEffect(self, effectString):
        currstr = "\t\t" + effectString + "\r\n"
        self.effectLines = self.effectLines[:-len(currstr)]

    def getOutput(self, lines):
        inEffect = False
        fullOutput = ""
        for i in lines:
            if i == "\tEffect()\n\t{\r":
                inEffect = True
                fullOutput += self.effectLines + "\t}\n\r\n"
            if not inEffect:
                if i != "\t\tTRUE(Unknown=0x2)\r":
                    fullOutput += i + "\n"
            else:
                if i == "\t}\n\r":
                    inEffect = False
        return fullOutput

    def getTrainingOutput(self, lines):
        inEffect = False
        fullOutput = ""
        for i in lines:
            if i == "\tEffect()\n\t{\r":
                inEffect = True
                if self.blacklisted:
                    fullOutput += "\tEffect()\n\t{\r"
                fullOutput += self.effectLines
                fullOutput += self.origEffectLines+ "\t\t}\r\n\t\tScript_End()\r\n\t}\n\r\n"
            if not inEffect:
                if i != "\t\tTRUE(Unknown=0x2)\r":
                    fullOutput += i + "\n"
            else:
                if i == "\t}\n\r":
                    inEffect = False
        return fullOutput

    def getBlacklistedOutput(self, lines):
        inEffect = False
        fullOutput = ""
        if self.effectLines == "\tEffect()\n\t{\r\n":
            self.effectLines = self.effectLines + "\t}\n\r\n"
        for i in lines:
            if i == "\tEffect()\n\t{\r":
                inEffect = True
            if not inEffect:
                if i != "\t\tTRUE(Unknown=0x2)\r":
                    fullOutput += i + "\n"
            else:
                if i == "\t\tScript_End()\r":
                    fullOutput += self.effectLines
                    inEffect = False
                elif i == "\t}\n\r":
                    fullOutput += i + "\n"
                    inEffect = False
                else:
                    fullOutput += i + "\n"
        return fullOutput

    def getDamageRGB(self, damageStr, angleStr):
        damage = float(damageStr)
        angle = int(angleStr, 16)
        if 240 <= angle <= 300:
            red = self.getHexFloat(255)
            green = self.getHexFloat(0)
            blue = self.getHexFloat(230)
        elif damage == 0:
            red = self.getHexFloat(255)
            green = self.getHexFloat(255)
            blue = self.getHexFloat(255)
        elif damage > 15:
            red = self.getHexFloat(255)
            green = self.getHexFloat(0)
            blue = self.getHexFloat(0)
        else:
            red = self.getHexFloat(255)
            green = self.getHexFloat(230 - (damage * 230 / 15))
            blue = self.getHexFloat(0)

        return red, green, blue

    def addDodgeEffects2(self, dodgeActive):
        self.addEffect(asynchronousTimer.format(dodgeActive[0]))
        self.addEffect(colorOverlay.format(*BLUE))
        self.addEffect(asynchronousTimer.format(str(int(dodgeActive[1]) + 1)))
        self.addEffect(terminateOverlays)
        self.addEffect(scriptEnd)

    def addDodgeEffects(self, dodgeActive, dodgeFAF):
        # starting frames
        self.addEffect(colorOverlay.format(*GREEN))
        # invuln
        self.addEffect(asynchronousTimer.format(dodgeActive[0]))
        self.addEffect(terminateOverlays)
        self.addEffect(colorOverlay.format(*BLUE))
        self.addEffect(asynchronousTimer.format(str(int(dodgeActive[1]) + 1)))
        self.addEffect(terminateOverlays)
        # lag
        self.addEffect(colorOverlay.format(*GREEN))
        self.addEffect(asynchronousTimer.format(dodgeFAF))
        self.addEffect(terminateOverlays)
        self.addEffect(scriptEnd)

    def addLagEffects(self, lagLength):
        if self.isInt(lagLength):
            self.addEffect(asynchronousTimer.format("1"))
            self.addEffect(colorOverlay.format(*GREEN))
            self.addEffect(asynchronousTimer.format(str(int(lagLength) + 1)))
            self.addEffect(terminateOverlays)
        self.addEffect(scriptEnd)

    def processFile(self, isBlacklisted=False, isTrainingOnly=False, isWeapon=False):
        self.weaponBool = isWeapon

        filename = self.filePath
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
        noBufferAnimations = {"FuraFura.acm", "FuraFuraStartD.acm", "FuraFuraStartD.acm", "0xE42E1C1E.acm", "StepJump.acm", "0xE0D78C1E", "StepFall.acm", "0xAD2064E4.acm"} # StepAirPose?, DownSpotU/DownSpotD
        hitstunAnimations = {"DamageAir1.acm", "DamageAir2.acm", "DamageAir3.acm", "DamageElec.acm", "DamageFlyHi.acm", "DamageFlyLw.acm", "DamageFlyN.acm", "DamageFlyTop.acm", "DamageHi1.acm", "DamageHi2.acm", "DamageHi3.acm", "DamageLw1.acm", "DamageLw2.acm", "DamageLw3.acm", "DamageN1.acm", "DamageN2.acm", "DamageN3.acm", "WallDamage.acm"}
        upTaunts = {"AppealHiL.acm", "AppealHiR.acm"}
        sideTaunts = {"AppealSL.acm", "AppealSR.acm"}
        downTaunts = {"AppealLwL.acm", "AppealLwR.acm"}
        fallingAnimations = {"Fall.acm", "FallSpecial.acm"}
        tumble = "DamageFall.acm"
        specialFall = "FallSpecial.acm"
        ledgegetup = "CliffClimbQuick.acm"
        ledgeroll = "CliffEscapeQuick.acm"
        ledgejump = "CliffJumpQuick1.acm"
        ledgeattack = "CliffAttackQuick.acm"
        ledgewait = "CliffWait.acm"
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
            self.blacklisted = True
            self.effectLines = ""

        if isTrainingOnly:
            if basename in {"EntryR.acm", "EntryL.acm"}:
                self.addEffect(basicVariableSet.format("0x0", showFullModVar))
                self.addEffect(basicVariableSet.format("0x0", hasEnteredVar))

        if not self.shouldProcessVariables and not self.weaponBool and not self.wifiSafe:
            self.trainingOnly = True
            if basename in upTaunts or basename.startswith("Wait"):
                self.addEffect(basicCompare.format(hasEnteredVar, notEqualTo, "0x0"))
            elif basename in sideTaunts or basename in downTaunts or basename in noBufferAnimations or basename.startswith("Wait"):
                self.addEffect(basicCompare.format(showFullModVar, greaterThanOrEqualTo, "0x1"))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                self.addEffect(basicCompare.format(showFullModVar,lessThanOrEqualTo, "0x2"))
            else:
                self.addEffect(basicCompare.format(showFullModVar, equalTo, "0x1"))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1

        with open(filename, newline="\r\n") as f:
            lines = f.readlines()
        lines = [x.strip('\n') for x in lines]
        if self.trainingOnly:
            self.parseForEffect(lines)
        for l in lines:
            self.myLines.append(l)

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
                            self.FAFIndex = 2
                            while not self.isInt(currFile[self.FAFIndex]):
                                self.FAFIndex = self.FAFIndex + 1
                            self.invStartIndex = self.FAFIndex + 1
                            self.invEndIndex = self.invStartIndex + 1
                            self.FAF = int(currFile[self.FAFIndex]) if int(currFile[self.FAFIndex]) != 0 else self.FAF
                            self.invStart = int(currFile[self.invStartIndex]) if int(currFile[self.invStartIndex]) != 0 else self.invStart
                            if int(currFile[self.invEndIndex]) != 0:
                                self.invStart = int(currFile[self.invStartIndex])
                                self.invEnd = int(currFile[self.invEndIndex])
                            if (charName in counterChars and basename == "SpecialLw.acm") or charName == "peach" and basename == "SpecialN.acm":
                                self.invStart = 10000
                                self.invEnd = 10000
                        tsvLines.append(line)
                    # tsvLines = tsv.readlines()
                tsvLines = [x.strip('\n') for x in tsvLines]
                paramsIndex = tsvLines.index("PARAMS SECTION")
                self.hurtboxesIndex = tsvLines.index("BONES SECTION")

                for h in range(self.hurtboxesIndex+2,len(tsvLines)):
                    currVals = tsvLines[h].split("\t")
                    currHurtboxList = []
                    for index in range(len(currVals)):
                        if index > 0:
                            currHurtboxList.append(currVals[index])
                    self.hurtboxes[currVals[0]] = currHurtboxList

        # self.addHurtboxes()

        inputIndex = filename.find("Input")
        edgeCaseFilename = filename[:inputIndex] + filename[inputIndex+len("Input/animcmd/"):]

        if self.didHandleEdgeCase(edgeCaseFilename):
            pass
        elif basename == ledgewait:
            for i in range(1, 150):
                self.addEffect(asynchronousTimer.format(i))
                self.addEffect(floatVariableSet.format(i, ledgeWaitFrameVar))
            self.addEffect(scriptEnd)
        elif basename in noBufferAnimations:
            self.addEffect(floatCompare.format(noBufferVar, lessThanOrEqualTo, self.getHexFloat(19.0)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(floatVariableSet.format(20.0, noBufferVar))
            self.inCompare -= 1
            self.addEffect('}')
            self.inCompare -= 1
            self.addEffect('}')
            self.addEffect(scriptEnd)
        elif basename.startswith("Wait") and not self.weaponBool:
            self.addEffect(basicCompare.format(showFullModVar, greaterThanOrEqualTo, hex(4)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(colorOverlay.format(*RED))
            self.addEffect(basicVariableSet.format(hex(1), showFullModVar))
            #self.addEffect(basicVariableSet.format(hex(10), playerNumVar))
            self.inCompare -= 1
            self.addEffect('}')

            self.addEffect(basicCompare.format(mashToggleVar, greaterThanOrEqualTo, "0x3"))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(basicCompare.format(mashToggleVar,lessThanOrEqualTo, "0x4"))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(basicCompare.format(currentPercentVar, equalTo, hex(0)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            string = "POINT\n0"
            self.printString(string)
            self.inCompare -= 1
            self.addEffect("}")
            self.addEffect(FALSEComp.format("0x10"))
            self.inCompare += 1
            for digit in range(1,10):
                string = "POINT\n{}".format(digit)
                self.addEffect(basicCompare.format(currentPercentVar, equalTo, hex(digit)))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                self.printString(string)
                self.inCompare -= 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare = self.inCompare + 1
            self.inCompare -= 1
            while self.inCompare > 1:
                self.addEffect("}")
                self.inCompare = self.inCompare - 1
            self.addEffect("}")

            self.addEffect(basicCompare.format(mashToggleVar, notEqualTo, "0x3"))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(basicCompare.format(mashToggleVar, notEqualTo, "0x4"))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            self.addEffect(terminateGraphic57)
            self.inCompare -= 1
            self.addEffect('}')
            self.inCompare -= 1
            self.addEffect('}')

            self.addEffect(scriptEnd)
        elif basename in downTaunts and not self.weaponBool and not self.wifiSafe:
            mashDict = OrderedDict(
                [(0, [RED, "MASH\nAIRDODGE"]), (1, [GREEN, "MASH\nJUMP"]), (2, [BLUE, "RANDOM\nLEDGE"]), (3, [ORANGE, "DAMAGE\n+10"]), (4, [ORANGE, "DAMAGE\n+1"]), (5, [MAGENTA, "INFINITE\nSHIELD"]), (6, [WHITE, "NONE"])])
            numToggles = len(mashDict)
            self.addEffect(basicCompare.format(mashToggleVar, greaterThanOrEqualTo, hex(numToggles-1)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare += 1
            color = mashDict[0][0]
            string = mashDict[0][1]
            self.addEffect(colorOverlay.format(*color))
            self.printString(string)
            self.addEffect(basicVariableSet.format(hex(0), mashToggleVar))
            self.inCompare -= 1
            self.addEffect("}")
            self.addEffect(FALSEComp.format("0x10"))
            self.inCompare += 1
            for mashIndex in range(numToggles-1):
                currVal = mashIndex
                newVal = mashIndex+1
                color = mashDict[newVal][0]
                string = mashDict[newVal][1]
                self.addEffect(basicCompare.format(mashToggleVar, equalTo, hex(currVal)))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare += 1
                self.addEffect(basicVariableSet.format(hex(newVal), mashToggleVar))
                self.addEffect(colorOverlay.format(*color))
                self.printString(string)
                if newVal == numToggles - 2:
                    self.addEffect(floatVariableSet.format("0", shieldDamageMultVar))
                    self.addEffect(floatVariableSet.format("0", shieldDegenVar))
                    self.addEffect(floatVariableSet.format("0", shieldRegenVar))
                elif newVal == numToggles - 1:
                    self.addEffect(floatVariableSet.format("1.19", shieldDamageMultVar))
                    self.addEffect(floatVariableSet.format("0.13", shieldDegenVar))
                    self.addEffect(floatVariableSet.format("0.08", shieldRegenVar))
                self.inCompare -= 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare = self.inCompare + 1
            self.inCompare -= 1
            while self.inCompare > 1:
                self.addEffect("}")
                self.inCompare = self.inCompare - 1
            self.addEffect("}")
            self.addEffect(asynchronousTimer.format(30))
            self.addEffect(allowInterrupt)
            self.addEffect(asynchronousTimer.format(30))
            self.addEffect(terminateGraphic57)
            self.addEffect(scriptEnd)
        elif basename in upTaunts and not self.weaponBool and not self.wifiSafe:
            effectToggleLines = ""
            effectToggleLines = self.addEffectToString(basicCompare.format(showFullModVar, equalTo, "0x0"), effectToggleLines)

            effectToggleLines = self.addEffectToString(TRUEComp.format("0x12"), effectToggleLines)
            self.inCompare += 1
            effectToggleLines = self.addEffectToString(colorOverlay.format(*RED), effectToggleLines)
            for segment in self.printString("FULL\nMOD", True):
                effectToggleLines = self.addEffectToString(segment, effectToggleLines)
            effectToggleLines = self.addEffectToString(basicVariableSet.format("0x1", showFullModVar), effectToggleLines)
            self.inCompare -= 1
            effectToggleLines = self.addEffectToString("}", effectToggleLines)
            effectToggleLines = self.addEffectToString(FALSEComp.format("0x10"), effectToggleLines)
            self.inCompare += 1
            effectToggleLines = self.addEffectToString(basicCompare.format(showFullModVar, equalTo, "0x1"), effectToggleLines)
            effectToggleLines = self.addEffectToString(TRUEComp.format("0x12"), effectToggleLines)
            self.inCompare += 1
            effectToggleLines = self.addEffectToString(colorOverlay.format(*GREEN), effectToggleLines)
            for segment in self.printString("HITBOXES\nVIS OFF", True):
                effectToggleLines = self.addEffectToString(segment, effectToggleLines)
            effectToggleLines = self.addEffectToString(basicVariableSet.format("0x2", showFullModVar), effectToggleLines)
            self.inCompare -= 1
            effectToggleLines = self.addEffectToString("}", effectToggleLines)
            effectToggleLines = self.addEffectToString(FALSEComp.format("0x10"), effectToggleLines)
            self.inCompare += 1
            effectToggleLines = self.addEffectToString(basicCompare.format(showFullModVar, equalTo, "0x2"), effectToggleLines)
            effectToggleLines = self.addEffectToString(TRUEComp.format("0x12"), effectToggleLines)
            self.inCompare += 1
            effectToggleLines = self.addEffectToString(colorOverlay.format(*BLUE), effectToggleLines)
            for segment in self.printString("OVERLAY\nONLY", True):
                effectToggleLines = self.addEffectToString(segment, effectToggleLines)
            effectToggleLines = self.addEffectToString(basicVariableSet.format("0x3", showFullModVar), effectToggleLines)
            self.inCompare -= 1
            effectToggleLines = self.addEffectToString("}", effectToggleLines)
            effectToggleLines = self.addEffectToString(FALSEComp.format("0x10"), effectToggleLines)
            self.inCompare += 1
            effectToggleLines = self.addEffectToString(colorOverlay.format(*WHITE), effectToggleLines)
            for segment in self.printString("VANILLA", True):
                effectToggleLines = self.addEffectToString(segment, effectToggleLines)
            effectToggleLines = self.addEffectToString(basicVariableSet.format("0x0", showFullModVar), effectToggleLines)
            self.inCompare -= 1
            effectToggleLines = self.addEffectToString("}", effectToggleLines)
            self.inCompare -= 1
            effectToggleLines = self.addEffectToString("}", effectToggleLines)
            self.inCompare -= 1
            effectToggleLines = self.addEffectToString("}", effectToggleLines)
            effectToggleLines = self.addEffectToString(asynchronousTimer.format(30), effectToggleLines)
            effectToggleLines = self.addEffectToString(allowInterrupt, effectToggleLines)
            effectToggleLines = self.addEffectToString(asynchronousTimer.format(30), effectToggleLines)
            effectToggleLines = self.addEffectToString(terminateGraphic57, effectToggleLines)
            effectToggleLines = self.addEffectToString(scriptEnd, effectToggleLines)
            self.effectLines += effectToggleLines
        elif basename in sideTaunts and not self.weaponBool and not self.wifiSafe:
            # normal, 0,
            self.addEffect(basicCompare.format(mashToggleVar, equalTo, hex(3)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare+=1
            self.addEffect("Hitbox(ID=0x0, Part=0x0, Bone=0x0, Damage=10, Angle=0x4A, KBG=0x0, WBKB=0x0, BKB=0x0, Size=200, X=0, Y=0, Z=0, Effect=0x0, Trip=0, Hitlag=0, SDI=1, Clang=0x1, Rebound=0x1, ShieldDamage=0x0, SFXLevel=0x0, SFX=0x0,Ground/Air=0x3, Direct/Indirect=0x1, Type=0x4)")
            self.inCompare-=1
            self.addEffect("}")
            self.addEffect(FALSEComp.format("0x10"))
            self.inCompare+=1
            self.addEffect(basicCompare.format(mashToggleVar, equalTo, hex(4)))
            self.addEffect(TRUEComp.format("0x12"))
            self.inCompare+=1
            self.addEffect("Hitbox(ID=0x0, Part=0x0, Bone=0x0, Damage=1, Angle=0x4A, KBG=0x0, WBKB=0x0, BKB=0x0, Size=200, X=0, Y=0, Z=0, Effect=0x0, Trip=0, Hitlag=0, SDI=1, Clang=0x1, Rebound=0x1, ShieldDamage=0x0, SFXLevel=0x0, SFX=0x0,Ground/Air=0x3, Direct/Indirect=0x1, Type=0x4)")
            self.inCompare-=1
            self.addEffect("}")
            self.addEffect(FALSEComp.format("0x10"))
            self.inCompare+=1
            DIValues = [0.2, 0, 0.785398, 1.570796, 2.356194, -3.14159, -2.356194,  -1.570796, -0.785398,  10, 20, 0.2]
            DIDict = OrderedDict(
                [(0.2, WHITE), (-3.14159, BLACK), (2.356194, BLACK), (1.570796, BLACK), (0.785398, BLACK), (0, BLACK), (-0.785398, BLACK), (-1.570796, BLACK), (-2.356194, BLACK), (10, MAGENTA), (20, MAGENTA)])
            for DIindex in range(len(DIValues)-1):
                currVal = DIValues[DIindex]
                newVal = DIValues[DIindex+1]
                color = DIDict[newVal]
                self.addEffect(floatCompare.format(DIChangeVar, equalTo, self.getHexFloat(currVal)))
                self.addEffect(TRUEComp.format("0x12"))
                self.inCompare = self.inCompare + 1
                self.addEffect(floatVariableSet.format(newVal, DIChangeVar))
                self.addEffect(colorOverlay.format(*color))
                if color == BLACK:
                    self.addEffect(showAngle.format(0,-30*math.sin(-1*newVal)+10,30*math.cos(newVal),-1*math.degrees(newVal)))
                if color == MAGENTA:
                    if newVal == 10:
                        for i in range(1, len(DIValues)-3):
                            processingVal = DIValues[i]
                            self.addEffect(showAngle.format(0,-30*math.sin(processingVal)+10,30*math.cos(processingVal),math.degrees(processingVal)))
                    elif newVal == 20:
                        for processingVal in {0, -3.14159}:
                            self.addEffect(showAngle.format(0,-30*math.sin(processingVal)+10,30*math.cos(processingVal),math.degrees(processingVal)))
                self.inCompare = self.inCompare - 1
                self.addEffect("}")
                self.addEffect(FALSEComp.format("0x10"))
                self.inCompare = self.inCompare + 1
            self.inCompare -= 1
            while self.inCompare > 1:
                self.addEffect("}")
                self.inCompare = self.inCompare - 1
            self.addEffect("}")
            self.addEffect(asynchronousTimer.format(15))
            self.addEffect(allowInterrupt)
        elif basename == spinningAnim:
            self.addHitstunOverlays(spinning=True)
        elif basename in hitstunAnimations:
            self.addHitstunOverlays()
        elif basename == unshield:
            self.addLagEffects('7')
        elif basename == shieldDamage:
            self.addEffect(colorOverlay.format(*GREEN))
            self.addEffect(scriptEnd)
        elif basename == ledgecatch:
            self.addLagEffects('2')
        elif basename == groundedfootstoolPose:
            self.addLagEffects('8')
        elif basename == groundedfootstoolBack:
            self.addLagEffects('20')
        elif basename == tumble:
            self.addEffect(floatVariableSet.format(1, canReallyAnyActionVar))
            self.addEffect(scriptEnd)
        elif basename == specialFall:
            self.addEffect(colorOverlay.format(*GREEN))
            self.addEffect(scriptEnd)
        elif basename == spotdodge:
            self.addDodgeEffects(tsvLines[0].split("\t")[0:2], tsvLines[1].split("\t")[0])
        elif basename == froll:
            self.addDodgeEffects(tsvLines[2].split("\t")[0:2], tsvLines[3].split("\t")[0])
        elif basename == broll:
            self.addDodgeEffects(tsvLines[4].split("\t")[0:2], tsvLines[5].split("\t")[0])
        elif basename == airdodge:
            self.addDodgeEffects(tsvLines[6].split("\t")[0:2], tsvLines[7].split("\t")[0])
        elif basename == ledgejump:
            self.addDodgeEffects2(tsvLines[8].split("\t")[0:2])
        elif basename == ledgeroll:
            self.addDodgeEffects(tsvLines[10].split("\t")[0:2], tsvLines[11].split("\t")[0])
        elif basename == ledgegetup:
            self.addDodgeEffects(tsvLines[12].split("\t")[0:2], tsvLines[13].split("\t")[0])
        elif basename == jumpsquat:
            self.addLagEffects(tsvLines[16].split("\t")[0])
        elif basename == lightLanding:
            self.addLagEffects(tsvLines[17].split("\t")[0])
        elif basename == hardLanding:
            self.addLagEffects(tsvLines[18].split("\t")[0])
        elif basename == landingAirN:
            self.addLagEffects(tsvLines[19].split("\t")[0])
        elif basename == landingAirF:
            self.addLagEffects(tsvLines[20].split("\t")[0])
        elif basename == landingAirB:
            self.addLagEffects(tsvLines[21].split("\t")[0])
        elif basename == landingAirHi:
            self.addLagEffects(tsvLines[22].split("\t")[0])
        elif basename == landingAirLw:
            self.addLagEffects(tsvLines[23].split("\t")[0])
        elif basename == downStandU:
            self.addDodgeEffects(tsvLines[25].split("\t")[0:2], tsvLines[26].split("\t")[0])
        elif basename == downStandD:
            self.addDodgeEffects(tsvLines[27].split("\t")[0:2], tsvLines[28].split("\t")[0])
        elif basename == downForwardU:
            self.addDodgeEffects(tsvLines[29].split("\t")[0:2], tsvLines[30].split("\t")[0])
        elif basename == downForwardD:
            self.addDodgeEffects(tsvLines[31].split("\t")[0:2], tsvLines[32].split("\t")[0])
        elif basename == downBackU:
            self.addDodgeEffects(tsvLines[33].split("\t")[0:2], tsvLines[34].split("\t")[0])
        elif basename == downBackD:
            self.addDodgeEffects(tsvLines[35].split("\t")[0:2], tsvLines[36].split("\t")[0])
        elif basename == passive:
            self.addDodgeEffects(tsvLines[37].split("\t")[0:2], tsvLines[38].split("\t")[0])
        elif basename == passiveF:
            self.addDodgeEffects(tsvLines[39].split("\t")[0:2], tsvLines[40].split("\t")[0])
        elif basename == passiveB:
            self.addDodgeEffects(tsvLines[41].split("\t")[0:2], tsvLines[42].split("\t")[0])
        elif basename == downBoundU:
            self.addEffect(downEffect1)
            self.addEffect(downEffect2)
            self.addLagEffects(tsvLines[43].split("\t")[1])
        elif basename == downBoundD:
            self.addEffect(downEffect1)
            self.addEffect(downEffect2)
            self.addLagEffects(tsvLines[44].split("\t")[1])
        elif basename in {jabresetU, jabresetD}:
            self.addEffect(asynchronousTimer.format("1"))
            self.addEffect(colorOverlay.format(*GREEN))
            self.addEffect(scriptEnd)
        else:
            if basename == ledgeattack:
                self.addDodgeEffects2(tsvLines[14].split("\t")[0:2])
                # self.removeLastEffect(scriptEnd)
            index = 0
            while index < len(self.myLines):
                iorig = self.myLines[index]
                i = self.removeBeginningWhitespace(iorig)

                # print(i)

                if i == "Main()\n\t{\r":
                    inMain = True
                    if self.myLines[index + 1] == "\t}\n\r":
                        break
                if shouldExitLoop:
                    break
                if inMain:
                    paramList = self.getParamList(i)

                    if i.startswith("}"):
                        if self.inCompare:
                            if self.inCompare == 1 and self.trainingOnly:
                                if self.inLoop:
                                    self.inLoop = False
                                    self.addEffect(endLoopOrCompare)
                                else:
                                    inMain = False
                                    shouldExitLoop = True
                            else:
                                self.inCompare = self.inCompare - 1
                                self.addEffect(endLoopOrCompare)
                        elif self.inLoop:
                            self.inLoop = False
                            self.addEffect(endLoopOrCompare)
                        else:
                            inMain = False
                            shouldExitLoop = True

                    if i.startswith("If_Compare2"):
                        self.addEffect(ifCompare2.format(paramList[0], paramList[1], paramList[2]))
                    elif i.startswith("If_Compare"):
                        self.addEffect(ifCompare.format(paramList[0], paramList[1], paramList[2]))
                    if i.startswith("If_Bit_is_Set"):
                        self.addEffect(ifBitIsSet.format(paramList[0]))
                    if i.startswith("IS_EXIST_ARTICLE"):
                        self.addEffect(isExistArticle.format(paramList[0]))
                    if i.startswith("unk_477705C2"):
                        self.addEffect(basicCompare.format(paramList[0], paramList[1], paramList[2]))
                    if i.startswith("unk_2DA7E2B6"):
                        self.addEffect(floatCompare.format(paramList[0], paramList[1], paramList[2]))
                    if i.startswith("TRUE"):
                        self.addEffect(TRUEComp.format(paramList[0]))
                        self.inCompare = self.inCompare + 1
                    if i.startswith("unk_870CF021"):
                        self.addEffect(TRUEComp2.format(paramList[0]))
                        self.inCompare = self.inCompare + 1
                    if i.startswith("FALSE"):
                        self.addEffect(FALSEComp.format(paramList[0]))
                        self.inCompare = self.inCompare + 1
                    if i.startswith("Goto"):
                        self.addEffect(goto.format(-gotoNum))
                        gotoNum = 0

                    loop = "Set_Loop"
                    if i.startswith("Set_Loop"):
                        loopNum = int(paramList[0]) # if paramList[0] != "-1" else 0
                        self.addEffect(setLoop.format(loopNum))
                        self.inLoop = True

                    if i.startswith("Loop_Rest()"):
                        self.addEffect("Loop_Rest()")

                    if i.startswith("Set_Frame_Duration"):
                        self.addEffect(setFrameDuration.format(paramList[0]))

                    if i.startswith("Set_Armor"):
                        state = paramList[0]
                        if state == "0x0":
                            self.addEffect(terminateOverlays)
                        else:
                            self.addEffect(colorOverlay.format(*MAGENTA))

                    if i.startswith("Body_Collision"):
                        state = paramList[0]
                        if state == "0x0":
                            self.addEffect(terminateOverlays)
                        else:
                            self.addEffect(colorOverlay.format(*BLUE))

                    if i.startswith("Search_Collision"):
                        bone = paramList[2]
                        size = self.getHexFloat(float(paramList[3]) * 19 / 200)
                        z = self.getHexFloat(float(paramList[4]))
                        y = self.getHexFloat(float(paramList[5]))
                        x = self.getHexFloat(float(paramList[6]))
                        red, green, blue = self.getHexFloat(0), self.getHexFloat(255), self.getHexFloat(255)
                        self.addEffect(coloredHitbox.format(bone, z, y, x, size, red, green, blue))

                    if i.startswith("Subroutine"):
                        hashNum = paramList[0]
                        self.addEffect(subroutine.format(hashNum))

                    if i.startswith("External_Subroutine"):
                        hashNum = paramList[0]
                        self.addEffect(extsubroutine.format(hashNum))

                    if i.startswith("WAIT_LOOP_CLR()"):
                        self.addEffect("WAIT_LOOP_CLR()")

                    if i.startswith("Defensive_Collision"):
                        self.addEffect(colorOverlay.format(*RED))

                    if i.startswith("Bit_Variable_Set"):
                        var = paramList[0]
                        specialLw = "SpecialLw"
                        if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                            self.addEffect(colorOverlay.format(*RED))

                    if i.startswith("Bit_Variable_Clear"):
                        var = paramList[0]
                        specialLw = "SpecialLw"
                        if var == "0x2100000E" and basename[:len(specialLw)] == specialLw and charName in counterChars:  # counter
                            self.addEffect(terminateOverlays)
                            if self.didProcessEndlag(self.myLines, index, basename, tsvLines):
                                processedEndlag = True

                    if i.startswith("Terminate_Defensive_Collision"):
                        self.addEffect(terminateOverlays)
                        if self.didProcessEndlag(self.myLines, index, basename, tsvLines):
                            processedEndlag = True

                    if i.startswith("Basic_Variable_Set"):
                        if offsetBegin == 0 and paramList[1] == "0x1100000F":
                            offsetBegin = int(paramList[0], 16)
                            prevFrame = int(self.getParamList(self.getLastEffectString())[0])
                            self.removeLastEffect(asynchronousTimer.format(prevFrame))
                            self.addEffect(asynchronousTimer.format(prevFrame + offsetBegin))
                        elif paramList[1] == "0x11000010":
                            offsetEnd = int(paramList[0], 16)

                    if i.startswith("Asynchronous_Timer") and not processedEndlag:
                        self.currentFrame = int(paramList[0])
                        if self.currentFrame > self.FAF:
                            self.addEffect(asynchronousTimer.format(self.FAF))
                            self.addEffect(terminateOverlays)
                            self.FAF = 10000
                        if self.currentFrame > self.invStart:
                            self.addEffect(asynchronousTimer.format(self.invStart))
                            self.addEffect(colorOverlay.format(*BLUE))
                            self.invStart = 10000
                        if self.currentFrame > self.invEnd:
                            self.addEffect(asynchronousTimer.format(self.invEnd))
                            self.addEffect(terminateOverlays)
                            self.invEnd = 10000
                            if not self.moreHitboxesExist(self.myLines[index:]):
                                self.addEffect(colorOverlay.format(*GREEN))
                        if offsetEnd != 0:
                            self.addEffect(asynchronousTimer.format(offsetEnd + prevFrame))
                            self.addEffect(terminateGraphic13)
                            self.addEffect(asynchronousTimer.format(offsetBegin + int(paramList[0])))
                            prevFrame = int(paramList[0])
                        else:
                            self.addEffect(asynchronousTimer.format(paramList[0]))
                        if self.currentFrame == self.FAF:
                            self.addEffect(terminateOverlays)
                            self.FAF = 10000
                        if self.currentFrame == self.invStart:
                            self.addEffect(colorOverlay.format(*BLUE))
                            self.invStart = 10000
                        if self.currentFrame == self.invEnd:
                            self.addEffect(terminateOverlays)
                            self.invEnd = 10000
                            if not self.moreHitboxesExist(self.myLines[index:]):
                                self.addEffect(colorOverlay.format(*GREEN))
                    elif i.startswith("Synchronous_Timer") and not processedEndlag:
                        if self.isInt(paramList[0]):
                            self.currentFrame = self.currentFrame + int(paramList[0])
                            frameToAdd = int(paramList[0])
                        else:
                            index = index + 1
                            continue
                        if self.currentFrame > self.FAF:
                            self.addEffect(asynchronousTimer.format(self.FAF))
                            self.addEffect(terminateOverlays)
                            frameToAdd = self.currentFrame - self.FAF
                            self.FAF = 10000
                        if self.currentFrame > self.invStart:
                            self.addEffect(asynchronousTimer.format(self.invStart))
                            self.addEffect(colorOverlay.format(*BLUE))
                            frameToAdd = self.currentFrame - self.invStart
                            self.invStart = 10000
                        if self.currentFrame > self.invEnd:
                            self.addEffect(asynchronousTimer.format(self.invEnd))
                            self.addEffect(terminateOverlays)
                            frameToAdd = self.currentFrame - self.invEnd
                            self.invEnd = 10000
                            if not self.moreHitboxesExist(self.myLines[index:]):
                                self.addEffect(colorOverlay.format(*GREEN))
                        self.addEffect(synchronousTimer.format(frameToAdd))
                        if self.currentFrame == self.FAF:
                            self.addEffect(terminateOverlays)
                            self.FAF = 10000
                        if self.currentFrame == self.invStart:
                            self.addEffect(colorOverlay.format(*BLUE))
                            self.invStart = 10000
                        if self.currentFrame == self.invEnd:
                            self.addEffect(terminateOverlays)
                            self.invEnd = 10000
                            if not self.moreHitboxesExist(self.myLines[index:]):
                                self.addEffect(colorOverlay.format(*GREEN))

                    if i.startswith("Undo_Bone_Collision"):
                        self.addEffect(terminateGraphic31)

                    if i.startswith("Enable Action Status") or i.startswith("Remove_All_Hitboxes"):
                        self.addEffect(terminateGraphic13)
                        self.mainList = []
                        if self.didProcessEndlag(self.myLines, index, basename, tsvLines):
                            processedEndlag = True

                    if i.startswith("Terminate_Grab_Collisions"):
                        self.addEffect(terminateGraphic13)
                        self.mainList = []
                        if self.didProcessEndlag(self.myLines, index, basename, tsvLines):
                            processedEndlag = True

                    if i.startswith("Delete_Catch_Collision"):
                        self.addEffect(terminateGraphic13)
                        if index != self.origIndex + len(self.mainList):
                            self.removeFromMainList(paramList[0])
                            self.addListToMain(index)
                        if self.didProcessEndlag(self.myLines, index, basename, tsvLines):
                            processedEndlag = True

                    if i.startswith("Delete_Hitbox"):
                        self.addEffect(terminateGraphic13)
                        if index != self.origIndex + len(self.mainList):
                            self.removeFromMainList(paramList[0])
                            self.addListToMain(index)
                        if self.didProcessEndlag(self.myLines, index, basename, tsvLines):
                            processedEndlag = True

                    if i.startswith("Set_Bone_Intangability"):
                        bone = paramList[0]
                        self.addHurtboxIntangibility(bone)

                    if not self.blacklisted:
                        if i.startswith("Move_Hitbox"):
                            self.addMovedToMainList(i,index)
                            self.addEffect(terminateGraphic13)
                            self.addListToMain(index)

                        if i.startswith("Change_Hitbox_Size"):
                            self.addChangedToMainList(i,index)
                            self.addEffect(terminateGraphic13)
                            self.addListToMain(index)

                        if i.startswith("Hitbox") or i.startswith("Special_Hitbox") or i.startswith("Collateral_Hitbox"):
                            self.addToMainList(i,index)
                            bone = paramList[2]
                            size = self.getHexFloat(float(paramList[8]) * 19 / 200)
                            z = self.getHexFloat(float(paramList[9]))
                            y = self.getHexFloat(float(paramList[10]))
                            x = self.getHexFloat(float(paramList[11]))
                            red, green, blue = self.getDamageRGB(paramList[3], paramList[4])
                            self.addEffect(coloredHitbox.format(bone, z, y, x, size, red, green, blue))

                        if i.startswith("Extended_Hitbox"):
                            self.addToMainList(i,index)
                            bone = paramList[2]
                            size = self.getHexFloat(float(paramList[8]) * 19 / 200)
                            zinit = float(paramList[9])
                            yinit = float(paramList[10])
                            xinit = float(paramList[11])
                            zfinal = float(paramList[24])
                            yfinal = float(paramList[25])
                            xfinal = float(paramList[26])
                            for j in range(0, 4):
                                zcurr = self.getHexFloat(zinit + ((zfinal - zinit) / 3 * j))
                                ycurr = self.getHexFloat(yinit + ((yfinal - yinit) / 3 * j))
                                xcurr = self.getHexFloat(xinit + ((xfinal - xinit) / 3 * j))
                                red, green, blue = self.getDamageRGB(paramList[3], paramList[4])
                                self.addEffect(coloredHitbox.format(bone, zcurr, ycurr, xcurr, size, red, green, blue))

                        if i.startswith("Extended_Special_Hitbox"):
                            self.addToMainList(i,index)
                            bone = paramList[2]
                            size = self.getHexFloat(float(paramList[8]) * 19 / 200)
                            zinit = float(paramList[9])
                            yinit = float(paramList[10])
                            xinit = float(paramList[11])
                            zfinal = float(paramList[40])
                            yfinal = float(paramList[41])
                            xfinal = float(paramList[42])
                            for j in range(0, 8):
                                zcurr = self.getHexFloat(zinit + ((zfinal - zinit) / 7 * j))
                                ycurr = self.getHexFloat(yinit + ((yfinal - yinit) / 7 * j))
                                xcurr = self.getHexFloat(xinit + ((xfinal - xinit) / 7 * j))
                                red, green, blue = self.getDamageRGB(paramList[3], paramList[4])
                                self.addEffect(coloredHitbox.format(bone, zcurr, ycurr, xcurr, size, red, green, blue))

                    if i.startswith("Grab_Collision2"):
                        self.addToMainList(i, index)
                        bone = paramList[1]
                        size = self.getHexFloat(float(paramList[2]) * 19 / 200)
                        z = self.getHexFloat(float(paramList[3]))
                        y = self.getHexFloat(float(paramList[4]))
                        x = self.getHexFloat(float(paramList[5]))
                        self.addEffect(grabHitbox.format(bone, z, y, x, size))
                    elif i.startswith("Grab_Collision"):
                        self.addToMainList(i, index)
                        bone = paramList[1]
                        size = self.getHexFloat(float(paramList[2]) * 19 / 200)
                        z = self.getHexFloat(float(paramList[3]))
                        y = self.getHexFloat(float(paramList[4]))
                        x = self.getHexFloat(float(paramList[5]))
                        self.addEffect(grabHitbox.format(bone, z, y, x, size))

                    if i.startswith("Extended_Grab_Collision"):
                        self.addToMainList(i, index)
                        bone = paramList[1]
                        size = self.getHexFloat(float(paramList[2]) * 19 / 200)
                        zinit = float(paramList[3])
                        yinit = float(paramList[4])
                        xinit = float(paramList[5])
                        zfinal = zinit  # float(paramList[8]) #zinit??
                        yfinal = float(paramList[9])
                        xfinal = float(paramList[10])
                        for j in range(0, 3):
                            zcurr = self.getHexFloat(zinit + ((zfinal - zinit) / 2 * j))
                            ycurr = self.getHexFloat(yinit + ((yfinal - yinit) / 2 * j))
                            xcurr = self.getHexFloat(xinit + ((xfinal - xinit) / 2 * j))
                            self.addEffect(grabHitbox.format(bone, zcurr, ycurr, xcurr, size))

                    if self.inLoop and not i.startswith("Set_Loop()"):
                        thisParamList = self.getParamList(self.getLastEffectString())
                        if thisParamList[0] != "":
                            gotoNum = gotoNum + len(thisParamList) + 1
                        else:
                            gotoNum = gotoNum + len(thisParamList)

                    if i.startswith("Script_End()"):
                        if self.currentFrame < self.invStart and self.invStart != 10000:
                            self.addEffect(asynchronousTimer.format(self.invStart))
                            self.currentFrame = self.invStart
                            self.addEffect(terminateOverlays)
                            self.invStart = 10000
                        if self.currentFrame < self.invEnd and self.invEnd != 10000:
                            self.addEffect(asynchronousTimer.format(self.invEnd))
                            self.currentFrame = self.invEnd
                            self.addEffect(terminateOverlays)
                            self.addEffect(colorOverlay.format(*GREEN))
                            self.invEnd = 10000
                        if self.currentFrame < self.FAF and self.FAF != 10000:
                            self.addEffect(colorOverlay.format(*GREEN))
                            self.addEffect(asynchronousTimer.format(self.FAF))
                            self.currentFrame = self.FAF
                            self.addEffect(terminateOverlays)
                            self.FAF = 10000
                        if offsetBegin != 0:
                            self.addEffect(asynchronousTimer.format(prevFrame + offsetEnd))
                            self.addEffect(terminateGraphic13)
                        if not self.trainingOnly:
                            self.addEffect(scriptEnd)
                        inMain = False
                        shouldExitLoop = True
                index = index + 1

            if self.currentFrame < self.invStart and self.invStart != 10000:
                self.addEffect(asynchronousTimer.format(self.invStart))
                self.currentFrame = self.invStart
                self.addEffect(colorOverlay.format(*BLUE))
            if self.currentFrame < self.invEnd and self.invEnd != 10000:
                self.addEffect(asynchronousTimer.format(self.invEnd))
                self.currentFrame = self.invEnd
                self.addEffect(terminateOverlays)
                self.addEffect(colorOverlay.format(*GREEN))
            if self.currentFrame < self.FAF and self.FAF != 10000:
                self.addEffect(colorOverlay.format(*GREEN))
                self.addEffect(asynchronousTimer.format(self.FAF))
                self.currentFrame = self.FAF
                self.addEffect(terminateOverlays)
                self.FAF = 10000

        if self.trainingOnly:
            self.inCompare = 0
            self.addEffect("}")
            self.addEffect(FALSEComp.format("0x10"))
            return self.getTrainingOutput(lines)
        elif self.blacklisted:
            return self.getBlacklistedOutput(lines)
        else:
            return self.getOutput(lines)

    def didHandleEdgeCase(self, filename):
        # change "False" to "True" to test variables
        if not self.shouldProcessVariables:
            # special edge case: bayo up b not working in vanilla fix; doesn't work
            '''
            if filename == "bayonettabodySpecialHi.acm" and self.trainingOnly:
                self.effectLines = "\tEffect()\n\t{\r\n" + self.origEffectLines
                return True
            '''

            self.filePath = "edgeCaseCode/{}".format(filename)
            if os.path.isfile(self.filePath):
                with open(self.filePath, 'r') as file:
                    content = file.readlines()
                content = [x.strip('\n') for x in content]
                inEffect = False
                for line in content:
                    #line = self.removeBeginningWhitespace(line)
                    if line.startswith("\tEffect()"):
                        inEffect = True
                    elif inEffect and not line.startswith("\t{") and not line.startswith("\t}"):
                        self.addEffect(line[1:])
                    elif line.startswith("\t}"):
                        inEffect = False
                return True
        else:
            # variable testing
            basicVar = "0x100000AC"
            basicCompMethod = equalTo
            basicDict = OrderedDict(
                [(10, PINK), (6, RED), (5, ORANGE), (4, YELLOW), (3, GREEN), (2, BLUE), (1, CYAN), (0, MAGENTA)])
            floatVar = "0x2000234"
            floatCompMethod = "0x3"
            floatDict = OrderedDict([(90, PINK), (70, RED), (50, ORANGE), (30, YELLOW), (10, GREEN), (5, BLUE), (3, CYAN), (1, MAGENTA)])
            bitVar = "0x21000025"
            whichToProcess = "float"
            tauntsOnly = False
            if tauntsOnly and filename.find("Appeal") == -1:
                return True
            if whichToProcess == "bit":
                # bit variables, frames 1 through 100
                if self.variableEffectLines == "":
                    for i in range(1, 101):
                        self.addEffect(asynchronousTimer.format(i))
                        self.addEffect(ifBitIsSet.format(bitVar))
                        self.addEffect(TRUEComp.format("0x12"))
                        self.inCompare = self.inCompare + 1

                        self.addEffect(colorOverlay.format(*CYAN))

                        self.inCompare = self.inCompare - 1
                        self.addEffect("}")
                        self.addEffect(FALSEComp.format("0x10"))
                        self.inCompare = self.inCompare + 1
                        self.addEffect(colorOverlay.format(*RED))
                        self.inCompare -= 1
                        while self.inCompare:
                            self.addEffect("}")
                            self.inCompare = self.inCompare - 1
                        self.addEffect("}")
                    self.addEffect(scriptEnd)
                    self.variableEffectLines = self.effectLines
                else:
                    self.effectLines = self.variableEffectLines
            elif whichToProcess == "float":
                # float variables, frames 1 through 100
                if self.variableEffectLines == "":
                    for i in range(1, 101):
                        self.addEffect(asynchronousTimer.format(i))
                        for value in floatDict:
                            color = floatDict[value]
                            self.addEffect(floatCompare.format(floatVar, floatCompMethod, self.getHexFloat(value)))
                            self.addEffect(TRUEComp.format("0x12"))
                            self.inCompare = self.inCompare + 1

                            self.addEffect(colorOverlay.format(*color))

                            self.inCompare = self.inCompare - 1
                            self.addEffect("}")
                            self.addEffect(FALSEComp.format("0x10"))
                            self.inCompare = self.inCompare + 1
                        self.addEffect(colorOverlay.format(*WHITE))
                        self.inCompare -= 1
                        while self.inCompare:
                            self.addEffect("}")
                            self.inCompare = self.inCompare - 1
                        self.addEffect("}")
                    self.addEffect(scriptEnd)
                    self.variableEffectLines = self.effectLines
                else:
                    self.effectLines = self.variableEffectLines
            elif whichToProcess == "basic":
                # basic variables
                if self.variableEffectLines == "":
                    for i in range(1, 101):
                        self.addEffect(asynchronousTimer.format(i))
                        for value in basicDict:
                            color = basicDict[value]
                            self.addEffect(basicCompare.format(basicVar, basicCompMethod, hex(value)))
                            self.addEffect(TRUEComp.format("0x12"))
                            self.inCompare = self.inCompare + 1

                            self.addEffect(colorOverlay.format(*color))

                            self.inCompare = self.inCompare - 1
                            self.addEffect("}")
                            self.addEffect(FALSEComp.format("0x10"))
                            self.inCompare = self.inCompare + 1
                        self.addEffect(colorOverlay.format(*WHITE))
                        self.inCompare -= 1
                        while self.inCompare:
                            self.addEffect("}")
                            self.inCompare = self.inCompare - 1
                        self.addEffect("}")
                    self.addEffect(scriptEnd)
                    self.variableEffectLines = self.effectLines
                else:
                    self.effectLines = self.variableEffectLines
            return True
        return False

    def stretchChecker(self, char, bodyOrWeapon, move):
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

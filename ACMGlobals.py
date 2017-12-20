from collections import OrderedDict

gameChars = "bayonetta,captain,cloud,dedede,diddy,donkey,duckhunt,falco,fox,gamewatch,ganon,gekkouga,ike,kamui,kirby,koopa,koopajr,link,littlemac,lizardon,lucario,lucas,lucina,luigi,mario,mariod,marth,metaknight,mewtwo,murabito,ness,pacman,palutena,peach,pikachu,pikmin,pit,pitb,purin,reflet,robot,rockman,rosetta,roy,ryu,samus,sheik,shulk,sonic,szerosuit,toonlink,wario,wiifit,yoshi,zelda,miiswordsman,miifighter,miigunner".split(",")
counterChars = "gekkouga,ike,kamui,littlemac,lucario,lucina,marth,palutena,peach,roy,shulk".split(",")

# game code lines
asynchronousTimer = "Asynchronous_Timer(Frames={})"
synchronousTimer = "Synchronous_Timer(Frames={})"
setBoneIntangability = "EFFECT_FOLLOW_COLOR(unknown=0x1000031, unknown={}, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x0, unknown=0x3FC00000, unknown=0x1, unknown=0x0, unknown=0x0, unknown=0x437F0000)"
setHurtbox = "Graphic_Effect6(Graphic=0x1000013, Bone={}, Z={}, Y={}, X={}, ZRot=0, YRot=0, XRot=0, Size={}, Terminate=0x1, Unknown=0x420C0000)"
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
extsubroutine = "External_Subroutine(Unknown={})"
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
defaultTRUE = TRUEComp.format("0x12")
defaultFALSE = FALSEComp.format("0x10")
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

#[z,y,x]
Z_INPUT_POS = [0, 30, 20]
X_INPUT_POS = [0, 20, 20]
A_INPUT_POS = [0, 20, 15]
B_INPUT_POS = [0, 17, 10]
L_INPUT_POS = [0, 30, 2]
STICK_INPUT_POS = [0, 23, 5]

mashDict = OrderedDict(
    [(0, [RED, "MASH\nAIRDODGE"]),
     (1, [GREEN, "MASH\nJUMP"]),
     (2, [BLUE, "RANDOM\nLEDGE"]),
     (3, [ORANGE, "DAMAGE\n+10"]),
     (4, [ORANGE, "DAMAGE\n+1"]),
     (5, [MAGENTA, "INFINITE\nSHIELD"]),
     (6, [CYAN, "HOLD\nSHIELD"]),
     (7, [WHITE, "NONE"])])

# string to index
reverseMashDict = {}
for mashIndex in range(len(mashDict)):
    reverseMashDict[mashDict[mashIndex][1]] = mashIndex

equalTo = "0x0"
notEqualTo = "0x1"
lessThanOrEqualTo = "0x2"
greaterThanOrEqualTo = "0x3"
###???
lessThan = "0x4"
greaterThan = "0x5"

# toggle 0: none; 1: fullMod+DI+hitstunOverlay; 2:DI+hitstunOverlay; 3: inputDisplay
toggleNumVar = "0x1200004A" # brawl glide data param (originally 60)
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
platformDropTimeVar = "0x12000147"
platformRemainTimeVar = "0x12000148"
platformInvinciblityVar = "0x12000149"
noBufferVar = "0x2000218"
playerOneDamageVar = "0x2000230" # super mushroom size multiplier? orig 1.7
playerOneLockedDamageVar = "0x200023c" # poison mushroom voice pitch mult, orig 1.25
CPULockedDamageVar = "0x2000236"
shouldLockP1DamageVar = "0x2000239"
shouldLockCPUDamageVar = "0x200023a"
lockConditionsSetVar = "0x200023b"
hasSetDamageVar = "0x200000B7"
ourLaunchSpeedVar = "0x2000231" # related to super mushroom. orig 0.5
hitstunVar = "0x1000003E"
launchSpeedVar = "0x10000003" # launch speed basic
currentPercentVar = "0x11000010"
isPlayerOneVar = "0x200000B0"
shouldShowFullModVar = "0x200000B1"
zInputVar = "0x200000B2"
xInputVar = "0x200000B3"
aInputVar = "0x200000B4"
bInputVar = "0x200000B5"
rInputVar = "0x200000B6"
stickXInputVar = "0x11000012"
stickYInputVar = "0x11000013"
extraVar = "0x21000027" # some other ryu thing

# file associations
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
hitstunAnimations = {"DamageAir1.acm", "DamageAir2.acm", "DamageAir3.acm", "DamageElec.acm", "DamageFlyHi.acm", "DamageFlyLw.acm", "DamageFlyN.acm", "DamageFlyTop.acm", "DamageFlyRoll.acm", "DamageHi1.acm", "DamageHi2.acm", "DamageHi3.acm", "DamageLw1.acm", "DamageLw2.acm", "DamageLw3.acm", "DamageN1.acm", "DamageN2.acm", "DamageN3.acm", "WallDamage.acm"}
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

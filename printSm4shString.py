import sys, struct

showSegment = "EFFECT_FOLLOW_COLOR(unknown=0x1000057, unknown=0x0, unknown={}, unknown={}, unknown={}, unknown={}, unknown=0x0, unknown=0x0, unknown={}, unknown=0x1, unknown={}, unknown={}, unknown={})"
ifCompare = "If_Compare(Variable={}, Method={}, Variable2={})"
TRUEComp = "TRUE(Unknown={}){{"
FALSEComp = "FALSE(Unknown={}){{"

BLACK = ['0', '0', '0', '128']

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
    '-': [segmentDict[x] for x in ['g']],
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
effectLines = ""
inCompare = 0

def floatToHex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def getHexFloat(value):
    hexFloat = str(floatToHex(value)).upper()
    return "".join(c.lower() if (c == "X") else c for i, c in enumerate(hexFloat))

def printChar( charToPrint, lineNum, horizOffset, facingLeft=False, addToString=False):
    if facingLeft:
        segments = alphabetReversed[charToPrint]
    else:
        segments = alphabet[charToPrint]
    lineOffset = 40 - (lineNum * 16)
    savedSegments = []
    for segment in segments:
        z = getHexFloat(segment[0])
        y = getHexFloat(segment[1] + lineOffset)
        x = getHexFloat(segment[2] + horizOffset)
        zrot = getHexFloat(segment[3])
        size = getHexFloat(0.5)
        if len(segment) == 5:
            size = getHexFloat(segment[4])
        hexColor = [getHexFloat(int(x)) for x in BLACK][:-1]
        segmentEffect = showSegment.format(z,y,x,zrot,size,*hexColor)
        if not addToString:
            addEffect(segmentEffect)
        savedSegments.append(segmentEffect)
    return savedSegments

def printString( stringToPrint, addToString=True):
    global inCompare
    lineNum = 0
    horizOffset = 0
    charNum = 0

    facingLeft = True
    savedEffects = []
    savedEffects.append(ifCompare.format("0x0","0x4","0x0"))
    savedEffects.append(TRUEComp.format("0x12"))
    if not addToString:
        addEffect(ifCompare.format("0x0","0x4","0x0"))
        addEffect(TRUEComp.format("0x12"))
    inCompare+=1
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
            effects = printChar(char.upper(), lineNum, horizOffset, facingLeft, addToString)
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
            inCompare -= 1
            savedEffects.append("}")
            savedEffects.append(FALSEComp.format("0x10"))
            if not addToString:
                addEffect("}")
                addEffect(FALSEComp.format("0x10"))
            inCompare += 1
            facingLeft = False
    inCompare -= 1
    savedEffects.append("}")
    if not addToString:
        addEffect("}")
    return savedEffects

def addEffect(effectString):
    global effectLines
    effectLines = effectLines + "\t\t"
    tabs = inCompare
    for q in range(tabs):
        effectLines += "    "

    effectLines = effectLines + effectString + "\r\n"

def main():
    if len(sys.argv) != 2:
        print("Requires one argument, the string to be processed.")
        exit()
    printString(sys.argv[1])
    print(effectLines)

if __name__ == "__main__":
    main()

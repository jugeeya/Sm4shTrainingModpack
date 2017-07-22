import sys

def removeWhitespaceBeforeAndAfter(line):
    str = ""
    beginIndex = 0
    endIndex = 0
    for i in range(len(line)):
        if (line[i].isspace() == False and beginIndex == 0):
            beginIndex = i
        if (line[i] == ')'):
            endIndex = i
    return line[beginIndex:endIndex+1]

def main():
    if (len(sys.argv) != 2):
        print("Needs one argument: .acm move file path")
        exit()
    filename = sys.argv[1]
    with open(filename, newline="\r\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    inEffect = False
    tabs = 0

    for i in lines:
        removed = removeWhitespaceBeforeAndAfter(i)
        # firstChar = removed[0] if len(removed) >= 1 else ''
        if removed[:len("TRUE")] == "TRUE" or removed[:len("FALSE")] == "FALSE":
            removed = removed + "{"
        if removed == "":
            removed = "}"
            if inEffect:
                tabs = tabs - 1
        for t in range(tabs):
            removed = "\t" + removed
        if inEffect:
            print("addEffect(\"",end="")
            print(removed,end="")
            print("\")",end="\n")
        trueIndex = removed.find("TRUE")
        falseIndex = removed.find("FALSE")
        if removed[tabs:tabs+len("TRUE")] == "TRUE":
            if inEffect:
                tabs = tabs + 1
        if removed[tabs:tabs+len("FALSE")] == "FALSE":
            if inEffect:
                tabs = tabs + 1
        setLoopIndex = removed.find("Set_Loop")
        if removed[tabs:len("Set_Loop")] == "Set_Loop":
            if inEffect:
                tabs = tabs + 1
        if removed == "Effect()":
            inEffect = True
        if removed == "Script_End()":
            inEffect = False
            
main()

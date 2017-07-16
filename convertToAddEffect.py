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

    for i in lines:
        removed = removeWhitespaceBeforeAndAfter(i)
        if removed[:len("TRUE")] == "TRUE" or removed[:len("FALSE")] == "FALSE":
            removed = removed + "{"
        if removed == "":
            removed = "}"
        if inEffect:
            print("addEffect(\"",end="")
            print(removed,end="")
            print("\")",end="\n")
        if removed == "Effect()":
            inEffect = True
        if removed == "Script_End()":
            inEffect = False
            
main()

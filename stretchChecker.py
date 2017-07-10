import sys

def main():
    if (len(sys.argv) != 3):
        print("Needs two arguments: char name and .acm move name")
        exit()
    charName = sys.argv[1]
    moveName = sys.argv[2]

    with open("blacklist/blacklist.tsv", newline="\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    inChar = False
    foundCharAndMove = False
    
    for i in lines:
        if (i[:len(charName)] == charName):
            inChar = True
        elif (i[0] == "\t" and inChar == True):
            if (i[1:] == moveName):
                print("blacklisted",end="")
                foundCharAndMove = True
        else:
            inChar = False
                        
    if (foundCharAndMove == False):
        print("okay",end="")

main()

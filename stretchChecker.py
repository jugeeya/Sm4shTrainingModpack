import sys

def main():
    if (len(sys.argv) != 4):
        print("Needs three arguments: char name, body/weapon, and .acm move name")
        exit()
    charName = sys.argv[1]
    bodyWeaponName = sys.argv[2]
    moveName = sys.argv[3]

    with open("blacklist/blacklist.tsv", newline="\n") as f:
        lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

    inChar = False
    inBodyWeapon = False
    foundCharAndMove = False
    
    for i in lines:
        if i.startswith(moveName):
            print("noprocess", end="")
            foundCharAndMove = True
            exit()
        if (i[:len(charName)] == charName):
            inChar = True
        elif (i[0] == "\t" and inChar == True):
            if (i[1:] == bodyWeaponName):
                inBodyWeapon = True
            elif (i[0:2] == "\t\t" and inBodyWeapon == True):
                if (i[2:] == moveName or i[2:] == "*"):
                    print("blacklisted",end="")
                    foundCharAndMove = True
                    exit()
            else:
                inBodyWeapon = False
        else:
            inChar = False
                        
    if (foundCharAndMove == False):
        print("okay",end="")

main()

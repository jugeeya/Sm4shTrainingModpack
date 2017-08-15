import sys

def main():
    if len(sys.argv) != 2:
        print("Needs one argument, edge case filepath")
    filename = sys.argv[1]
    outputIndex = filename.find("Output")
    edgeCaseFilename = filename[:outputIndex] + filename[outputIndex+len("Output/animcmd/"):]
    with open(filename, 'r') as file:
        data = file.read()
    outputFile = open("edgeCaseCode/{}".format(edgeCaseFilename), 'w')
    outputFile.write(data)
    outputFile.close()

main()
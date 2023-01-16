# Wesley Reynolds
# CSC - 492


# Library dependencies
import sys


# This method displays the intended program usage and exits the program
# --> exit()
def invalidProgramUsage():
    print("USAGE: replaceSVGInHTML.py HTML_FILEPATH SVG_FILEPATH")
    print("WHERE: HTML_FILEPATH is the path of a html file containing an <svg> object")
    print("WHERE: SVG_FILEPATH is the path of a svg file containing an <svg> object")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string, string
def checkArgv(argv):
    if len(argv) != 4:
        invalidProgramUsage()
    else:
        return argv[1], argv[2], argv[3]


# This program replaces the <svg> object in an html file with the <svg> object in an svg file
# string[] --> int
def main(argv):
    # Check for valid program usage and open needed files
    indexHtmlFilepath, newHtmlFilepath, svgFilepath = checkArgv(argv)
    indexHtmlFP = open(indexHtmlFilepath, "r")
    svgFP = open(svgFilepath, "r")

    # Create a string containing the <svg> object
    svg = "\t"
    line = svgFP.readline()
    while line != "":
        svg += line
        line = svgFP.readline()
    svg += "\n"

    # Create a string containing the data to write to the html file
    outContents = ""
    inSVG = False
    line = indexHtmlFP.readline()
    while line != "":
        tokens = line.split()
        if len(tokens) > 0:           
            if tokens[0].strip() == "<svg":
                inSVG = True
                outContents += svg
            if tokens[0].strip() == "</svg>":
                inSVG = False
                line = indexHtmlFP.readline()
        if not inSVG:
            outContents += line
        line = indexHtmlFP.readline()


    # Reopen the html file in write mode and write the new contents
    indexHtmlFP.close()
    newHtmlFP = open(newHtmlFilepath, "w")
    newHtmlFP.write(outContents)

    # Close files and exit program
    newHtmlFP.close()
    svgFP.close()
    return 0


# The driver routine for the program
if __name__ == "__main__":
    print("Program Execution Started")
    if main(sys.argv) == 0:
        print("Program Execution Terminated Successfully")
    else:
        print("Program Execution Terminated Abnormally")
# Wesley Reynolds
# CSC - 492


# Library dependencies
import sys
import mysql.connector
import writeNoColorSVG


# Given a string that represents a number, this method returns the string with commas
# string --> string
def stringToNum(stringNum):
    num = ""
    j = 0
    if "." in stringNum:
        return stringNum
    for i in range(len(stringNum)-1, -1, -1):
        num = stringNum[i] + num
        j += 1
        if j == 3 and i != 0:
            num = "," + num
            j = 0
    return num


# Given an SQL column name, this method returns the values to use for the Color Map Key on that column.
# string, int --> string[]
def getColorKeys(colName, year):
    colorKeys = []
    buckets = [0, 55, 112, 169, 226, 283, 340, 397, 454, 511]

    host = "localhost"
    user = "root"
    password = "Valentino46"
    database = "seniorproject"
    db = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()

    for i in range(1, len(buckets)):
        maxQuery = "SELECT MAX(%s) FROM Counties WHERE year = %s AND %sBucket <= %d;" % (colName, year, colName, buckets[i])
        cursor.execute(maxQuery)
        result = cursor.fetchall()
        maxValue = stringToNum(str(int(result[0][0])))

        minQuery = "SELECT MIN(%s) FROM Counties WHERE year = %s AND %sBucket >= %d;" % (colName, year, colName, buckets[i-1])
        cursor.execute(minQuery)
        result = cursor.fetchall()
        minValue = stringToNum(str(int(result[0][0])))

        value = minValue + " - " + maxValue
        colorKeys.append(value)

    return colorKeys


# This method displays the intended program usage and exits the program
# --> exit()
def invalidProgramUsage():
    print("USAGE: createColoredHTML.py HTML_FILEPATH YEAR COL_NAME OUTPUT_PATH")
    print("WHERE: HTML_FILEPATH is the path of the base html file")
    print("WHERE: YEAR is year of the data to make a map of")
    print("WHERE: COL_NAME is the name of the SQL column to be colored")
    print("WHERE: OUTPUT_PATH is the path of the desired output file")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string, string
def checkArgv(argv):
    if len(argv) != 5:
        invalidProgramUsage()
    else:
        return argv[1], argv[2], argv[3], argv[4]


# This program replaces the <svg> object in an html file with the <svg> object in an svg file
# string[] --> int
def main(argv):
    # Check for valid program usage and open needed files
    baseHTMLFilepath, year, colName, outputFilepath = checkArgv(argv)
    baseFP = open(baseHTMLFilepath, "r")
    outFP = open(outputFilepath, "w")

    # Define the buttons to be included in color maps
    onclick = "onclick=\"window.location.href='C:/Users/wesre/Documents/Cal%20Poly/CSC/492/gitRepo/CSC-492/WebApp/NoColorMaps/" + year + ".html';\""
    buttons = "\t%s\n\t\t%s\n\t\t%s\n\t\t%s\n\t%s\n\n" % ("<button class=\"NoColorMap\" type=\"button\"",
                                              onclick,
                                              "style=\"position: absolute; right: 0\">",
                                              "Remove Coloring",
                                              "</button>")

    # Get the Color Map Key Values from the SQL DB
    colorKeys = getColorKeys(colName, year)

    # Define the Color Map Key (Top Left)
    key = "\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\t%s\n\n" % (
                                                      "<div id=\"ColorKeyTitle\">%s</div>" % (writeNoColorSVG.colNameToKeyTitle(colName)),
                                                      "<div id=\"ColorKey1\">%s</div>" % (colorKeys[0]),
                                                      "<div id=\"ColorKey2\">%s</div>" % (colorKeys[1]),
                                                      "<div id=\"ColorKey3\">%s</div>" % (colorKeys[2]),
                                                      "<div id=\"ColorKey4\">%s</div>" % (colorKeys[3]),
                                                      "<div id=\"ColorKey5\">%s</div>" % (colorKeys[4]),
                                                      "<div id=\"ColorKey6\">%s</div>" % (colorKeys[5]),
                                                      "<div id=\"ColorKey7\">%s</div>" % (colorKeys[6]),
                                                      "<div id=\"ColorKey8\">%s</div>" % (colorKeys[7]),
                                                      "<div id=\"ColorKey9\">%s</div>" % (colorKeys[8])
                                                      )	

    # Define the target to indicate a FILL
    targetLine = "%s.innerHTML =" % (colName)

    # Write the (modified) contents to the new file
    linkFound = False
    inButtons = False
    inSlider = False
    buttonsWritten = False
    line = baseFP.readline()
    while line != "":
        if not linkFound:
            if "link" in line:
                line = "\t<link rel=\"stylesheet\" href=\"../../Styles/indexStyle.css\">"
                linkFound = True
        if "button" in line and not buttonsWritten:
            inButtons = True
        if "slider" in line:
            inSlider = True
        if inSlider:
            if "input" in line and "oninput" not in line:
                line = "\t\t<input type=\"range\" min=\"2017\" max=\"2025\" value=\""+ year +"\"\n"
            elif "var newPath = window.location.href.slice(0, -9)" in line:
                line = "var basePath = window.location.href.split('/').slice(0,-2);\nbasePath = basePath.join('/');\nvar page = window.location.href.split('/').slice(-1)[0];\nvar newPath = basePath.concat('/', this.value , '/', page);\n"
            elif "rangeValue" in line and "innerText" not in line:
                line = "\t\t<p id=\"rangeValue\">"+ year + "</p>\n"
            if "/div" in line:
                inSlider = False
        if "svg" in line:
            inButtons = False
            if not buttonsWritten:
                outFP.write(buttons + key)    # Write the "Remove Coloring" button and the Key
                buttonsWritten = True
        if targetLine in line:
            line += "\n\t\t\t\t\tdocument.getElementById(\"%s\").style.color = \"#E813A8\";" % (colName)    # Add color to bottom right data
        if not inButtons:
            if "NoColorMaps" in line:
                tokens = line.split("/")
                buttonYear = tokens[-1].split(".")[0]
                line = ""
                for token in tokens[:-2]:
                    line += token + "/"
                line += "ColorMaps/"+buttonYear+"/"+colName+".html';\"\n"
            outFP.write(line)
        line = baseFP.readline()

    # Close files and exit program
    baseFP.close()
    outFP.close()
    return 0


# The driver routine for the program
if __name__ == "__main__":
    print("Program Execution Started")
    if main(sys.argv) == 0:
        print("Program Execution Terminated Successfully")
    else:
        print("Program Execution Terminated Abnormally")
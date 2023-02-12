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
    buckets = [0, 63, 127, 191, 255, 319, 383, 447, 511]
    if colName == "crimeRate":
        buckets[0] = 26
    elif colName == "medianHouseholdIncome":
        buckets[0] = 10
    elif colName == "percentNeedOpioidTreatment":
        buckets[0] = 13
    elif colName == "sexRatio":
        buckets[-1] = 510

    host = "localhost"
    user = "root"
    password = "Valentino46"
    database = "seniorproject"
    db = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()

    for bucket in buckets:
        query = "SELECT MAX(%s) FROM Counties WHERE year = %s AND %sBucket <= %d;" % (colName, year, colName, bucket)
        cursor.execute(query)
        result = cursor.fetchall()
        value = stringToNum(str(int(result[0][0])))
        colorKeys.append(value)

    return colorKeys


# This method displays the intended program usage and exits the program
# --> exit()
def invalidProgramUsage():
    print("USAGE: createColoredHTML.py HTML_FILEPATH YEAR OUTPUT_PATH")
    print("WHERE: HTML_FILEPATH is the path of the base html file")
    print("WHERE: YEAR is year of the data to make a map of")
    print("WHERE: OUTPUT_PATH is the path of the desired output file")
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
    baseHTMLFilepath, year, outputFilepath = checkArgv(argv)
    baseFP = open(baseHTMLFilepath, "r")
    outFP = open(outputFilepath, "w")

    # Write the (modified) contents to the new file
    linkFound = False
    inButtons = False
    inSlider = False
    line = baseFP.readline()
    while line != "":
        if not linkFound:
            if "link" in line:
                line = "\t<link rel=\"stylesheet\" href=\"../Styles/indexStyle.css\">"
                linkFound = True
        if "button" in line:
            inButtons = True
        if "svg" in line:
            inButtons = False
        if inButtons:
            if "ColorMaps" in line and "NoColorMaps" not in line:
                colName = line.split("/")[-1].split(".")[0]
                line = "onclick=\"window.location.href='C:/Users/wesre/Documents/Cal%20Poly/CSC/492/gitRepo/CSC-492/WebApp/ColorMaps/"+year+"/"+colName+".html';\"\n"
        if "slider" in line:
            inSlider = True
        if inSlider:
            if "input" in line and "oninput" not in line:
                line = "\t\t<input type=\"range\" min=\"2017\" max=\"2025\" value=\""+ year +"\"\n"
            elif "rangeValue" in line and "innerText" not in line:
                line = "\t\t<p id=\"rangeValue\">"+ year + "</p>\n"
            if "/div" in line:
                inSlider = False
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
# Wesley Reynolds
# CSC - 492


# Included libraries
import sys
import mysql.connector


# Given an integer in [0, 256), this method returns the appropriate hex string
# int --> string
def hexValueToString(value):
    hexString = "%x" % (value)
    if len(hexString) == 1:
        hexString = "0" + hexString
    return hexString


# Given a bucket, return a string represent the color in HTML
# int --> string
def getColor(bucket):
    if bucket <= 255:
        if bucket <= 127:
            redValue = 255
            greenValue = bucket * 2
        else:
            redValue = 255 - ((bucket - 128) * 2)
            greenValue = 255
        blueValue = 0
    else:
        if bucket <= 383:
            greenValue = 255
            blueValue = (bucket - 255) * 2
        else:
            greenValue = 255 - ((bucket - 384) * 2)
            blueValue = 255
        redValue = 0

    redHex = hexValueToString(redValue)
    greenHex = hexValueToString(greenValue)
    blueHex = hexValueToString(blueValue)

    return "#" + redHex + greenHex + blueHex


# This method displays the intended program usage and exits the program
def invalidProgramUsage():
    print("USAGE: writeNoColorSVG.py SVG_FILEPATH YEAR COL_NAME OUTPUT_PATH")
    print("WHERE: SVG_FILEPATH is the path of the svg file to modify")
    print("WHERE: YEAR is year of the SVG map to be created")
    print("WHERE: COL_NAME is name of the SQL column to be colored")
    print("WHERE: OUTPUT_PATH is the path resulting SVG file")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string
def checkArgv(argv):
    if len(argv) != 5:
        invalidProgramUsage()
    else:
        return argv[1], argv[2], argv[3], argv[4]


# Given MySQL DB credentials, this method returns a Dictionary mapping county names
# to Dictionaries that map SQL column names to values
# database credentials, year --> dictionary(string, dictionary(string, value))
def getMapFromDB(host, user, password, database, year):
    dataMap = {}

    db = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Counties WHERE year = %s" % year)
    columns = [i[0] for i in cursor.description]
    result = cursor.fetchall()

    for entry in result:
        valueMap = {}

        for i in range(len(columns)):
            valueMap[columns[i]] = entry[i]

        valueMap.pop("year")
        dataMap[entry[0]] = valueMap

    return dataMap


# Given a string that represents a number, this method returns the string with commas
# string --> string
def stringToNum(numString):
    if '.' in numString:
        return numString
    num = ""
    j = 0
    for i in range(len(numString)-1, -1, -1):
        num = numString[i] + num
        j += 1
        if j == 3 and i != 0:
            num = "," + num
            j = 0
    return num


# Given an SQL column name, return the string to use in the Title of the Color Map Key for that column
# string --> string
def colNameToKeyTitle(colName):
    titles = {"medianHomeValue": "Home Value ($)",
              "medianHouseholdIncome": "Household Income ($)",
              "percentHealthInsurance": "Health Insurance (%)",
              "percentHighSchool": "High School Grad (%)",
              "percentCollege": "College Grad (%)",
              "percentEmployed": "Employed (%)",
              "sexRatio": "Males (Per 100 Females)",
              "crimeRate": "Crime Rate (Per 100,000)",
              "percentNeedOpioidTreatment": "Need Opioid Treatment (%)",
              "averageOctoberTemperature": "October Temperature (F)"}
    
    return titles[colName]


# This program will make a copy and modify the given svg file to append data to each State object
def main(argv):
    # Check for valid program usage and open needed files
    inputSVGFilepath, year, columnName, outputFilepath = checkArgv(argv)
    inSVGFp = open(inputSVGFilepath, "r")
    outFP = open(outputFilepath, "w")

    # Get a Dictionary mapping counties to their data for a given year
    host = "localhost"
    user = "root"
    password = "Valentino46"
    database = "seniorproject"
    counties = getMapFromDB(host, user, password, database, year)

    # Skip past the data before <svg
    line = inSVGFp.readline()
    while "<svg" not in line:   # Don't include the header of the given svg file
        line = inSVGFp.readline()

    # Write modified <svg> object to new file
    while line != "":
        outFP.write(line)
        if "data-name=" in line:  # Include data right after the name of the state
            county = line.split("=")[1].strip().strip(">").strip("\"")
            if county in counties:
                values = counties[county]
                columns = values.keys()
                color = getColor(int(values[columnName+"Bucket"]))
                outFP.write("   fill=\"%s\"\n" % (color))
                for column in columns:
                    if column == "cid" or "Bucket" in column:
                        continue
                    outFP.write("   data-%s=\"%s: %s\"\n" % (column.lower(), colNameToKeyTitle(column), stringToNum(str(values[column]))))
            else:
                print("Missing key: ", county)
        line = inSVGFp.readline()

    # Close files and exit program
    inSVGFp.close()
    outFP.close()
    return 0


# The driver routine for the program
if __name__ == "__main__":
    print("Program Execution Started")
    if main(sys.argv) == 0:
        print("Program Execution Terminated Successfully")
    else:
        print("Program Execution Terminated Abnormally")
# Wesley Reynolds
# CSC - 492


# Included libraries
import sys
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# This method displays the intended program usage and exits the program
def invalidProgramUsage():
    print("USAGE: writeHistoryPNG.py COL_NAME OUTPUT_DIR")
    print("WHERE: COL_NAME is name of the SQL column to be visualized")
    print("WHERE: OUTPUT_DIR is the path of the directory to store the resulting PNG file")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string
def checkArgv(argv):
    if len(argv) != 3:
        invalidProgramUsage()
    else:
        return argv[1], argv[2]



# This method returns an array of county names
# string, string, string, string --> string[]
def getCounties(host, user, password, database):
    counties = []
    db = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT cid FROM Counties")
    result = cursor.fetchall()
    for entry in result:
        counties.append(entry[0])
    return counties


# This program will make a copy and modify the given svg file to append data to each State object
def main(argv):
    # Check for valid program usage and open needed files
    columnName, outputDir = checkArgv(argv)

    # Make a pandas Dataframe to represent the county data for the given column
    host = "localhost"
    user = "root"
    password = "Valentino46"
    database = "seniorproject"
    counties = getCounties(host, user, password, database)

    for countyName in counties:
        dictionary = {"Year": [],
                  columnName: []}
        outputFilepath = outputDir + "%s%s.png" % (columnName, countyName)
        db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = db.cursor()
        cursor.execute("SELECT %s, year FROM Counties WHERE cid = \"%s\"" % (columnName, countyName))
        result = cursor.fetchall()
        for entry in result:
            dictionary["Year"].append(entry[1])
            dictionary[columnName].append(entry[0])

        df = pd.DataFrame(dictionary)#, index=[0])

        # Use matplot to generate an image of the data
        df.plot(x="Year", y=columnName, kind="bar")

        # Save the image to a file
        plt.savefig(outputFilepath)

    # Close files and exit program
    return 0


# The driver routine for the program
if __name__ == "__main__":
    print("Program Execution Started")
    if main(sys.argv) == 0:
        print("Program Execution Terminated Successfully")
    else:
        print("Program Execution Terminated Abnormally")
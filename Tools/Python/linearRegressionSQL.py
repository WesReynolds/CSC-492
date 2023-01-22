# Wesley Reynolds
# CSC - 492


# Library dependencies
import sys
import mysql.connector
import dataMapsToSQL
import numpy as np
from sklearn.linear_model import LinearRegression


# This method displays the intended program usage and exits the program
# --> exit()
def invalidProgramUsage():
    print("USAGE: linearRegressionSQL.py DB_SOURCE_FILEPATH")
    print("WHERE: DB_SOURCE_FILEPATH is the filepath to Database Source")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string
def checkArgv(argv):
    if len(argv) != 2:
        invalidProgramUsage()
    else:
        return argv[1]


# This method reads from the SQL DB to generate a dictionary representing the linear regression data
# string, string, string, string --> {(string, string) --> {string --> float}}
def getLinearRegression(host, user, password, database, columns):
    # Instantiate dictionary
    linearReg = {}

    # Get an array of cid's
    db = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT cid FROM Counties")
    result = cursor.fetchall()
    counties = []
    for entry in result:
        counties.append(entry[0])

    # For each county, create a dictionary mapping year to a dictionary mapping column to value
    # Add this dictionary to linearReg
    for county in counties:
        cursor.execute("SELECT * FROM Counties WHERE cid = \"%s\" ORDER BY year" % county)
        result = cursor.fetchall()
        countyData = {}
        for entry in result:
            year = entry[1]
            countyYear = {}
            countyYear["cid"] = county
            countyYear["year"] = year
            i = 2
            for data in entry[2::2]:
                countyYear[columns[i]] = data
                i += 2
            countyData[year] = countyYear
        # With the data for the county, do the linear regression
        predYears = [2022, 2023, 2024, 2025]
        i = 0
        for year in predYears:
            # Make dictionary for year
            countyReg = {}
            for column in columns[2::2]:
                x = []
                y = []
                for dataYear in countyData.keys():
                    x.append(float(dataYear))
                    y.append(float(countyData[dataYear][column]))
                x = np.array(x).reshape(-1, 1)
                y = np.array(y)
                model = LinearRegression().fit(x, y)
                yPred = model.predict(np.array(predYears).reshape(-1, 1))
                countyReg["cid"] = county
                countyReg["year"] = year
                countyReg[column] = float(yPred[i])
            i += 1
            # Append dictionary for (county, year) to return dictionary
            linearReg[(county, year)] = countyReg

    # Return dictionary
    return linearReg


# Given a year and a column, this function returns a dictionary that maps the counties
# to the bucket values for that year.
# dictionary, int, string --> {county --> bucket}
def getBucketsForYearColumn(linearReg, year, column):
    buckets = {}
    values = []
    for entry in linearReg:
        if entry[1] == year:
            values.append(linearReg[entry][column])
    values.sort()
    bucketSize = len(values) / 512
    for i in range(len(values)):
        bucket = int(i // bucketSize)
        buckets[values[i]] = bucket

    countyBuckets = {}
    for entry in linearReg:
        if entry[1] == year:
            countyBuckets[entry[0]] = buckets[linearReg[entry][column]]
    return countyBuckets


# Given a linear regression dictionary, this method determines bucket values and adds them
# to the dictionary
# dictionary, string[] --> void
def addBuckets(linearReg, columns):
    buckets = {}
    years = [2022, 2023, 2024, 2025]
    for year in years:
        buckets[year] = {}
    for column in columns[2::2]:
        for year in years:
            buckets[year][column] = getBucketsForYearColumn(linearReg, year, column)   # dictionary that maps county to bucket value

    # Add bucket data to linear regression dictionary
    for entry in linearReg.keys():
        county = entry[0]
        year = entry[1]
        for column in columns[2::2]:
            linearReg[entry][column + "Bucket"] = buckets[year][column][county]

    return


# Given a dictionary that represent a tuple, return the INSERT string with ()
# dictionary, string[] --> string
def getInsertTuple(countyDict, columns):
    insertStr = "("
    for column in columns:
        if column == "cid":
            insertStr += "\"%s\"" % countyDict[column]
        else:
            insertStr += ", %s" % countyDict[column]
    insertStr += ")"
    return insertStr


# Given a file pointer and a list of ordered columns, this method uses the SQL DB to generate tuples for 
# INSERT statements in a linear regression of existing data.
# fp, string[] --> void
def writeInsertTuples(outFP, columns):
    # Define DB credentials
    host = "localhost"
    user = "root"
    password = "Valentino46"
    database = "seniorproject"

    # For each county, preform a linear regression to predict future data
    # {(cid, year) --> {column --> value}}
    linearReg = getLinearRegression(host, user, password, database, columns)
    
    # Using predictions, determine buckets and add them to data structure
    addBuckets(linearReg, columns)

    # Use predictions and buckets to generate and write tuples
    for key in linearReg.keys():
        outFP.write(getInsertTuple(linearReg[key], columns) + ",\n\t")

    return


# This program creates a map of the data in the given data filepath and writes the data to
# an SQL INSERT script
# string[] --> int
def main(argv):
    # Check for valid program usage and open needed files
    databaseSourceFilepath = checkArgv(argv)
    outFP = open(databaseSourceFilepath + "LinearRegression.sql", "w")

    # Write the header to the new SQL file
    columns = dataMapsToSQL.writeFillTablesHeader(outFP, databaseSourceFilepath + "CreateTables.sql")

    # Write the insert statement to the new SQL file
    writeInsertTuples(outFP, columns)
    outFP.close()
    outFP = open(databaseSourceFilepath + "LinearRegression.sql", "rb+")
    outFP.seek(-4, 2)
    outFP.truncate()
    outFP.close()
    outFP = open(databaseSourceFilepath + "LinearRegression.sql", "a")
    outFP.write(";\n")

    # Close files and exit program
    outFP.close()
    return 0


# The driver routine for the program
if __name__ == "__main__":
    print("Program Execution Started")
    if main(sys.argv) == 0:
        print("Program Execution Terminated Successfully")
    else:
        print("Program Execution Terminated Abnormally")
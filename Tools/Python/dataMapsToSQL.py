# Wesley Reynolds
# CSC - 492


# Library dependencies
import sys
import os


# This method displays the intended program usage and exits the program
# --> exit()
def invalidProgramUsage():
    print("USAGE: dataMapsToSQL.py DATA_DIRECTORY DATABASE_SOURCE_ROOT")
    print("WHERE: DATA_DIRECTORY (must end in '/') is the path of the directory with the files containing data to insert")
    print("WHERE: DATABASE_SOURCE_ROOT is the path of the root directory for the Database Source")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string
def checkArgv(argv):
    if len(argv) != 3:
        invalidProgramUsage()
    else:
        if argv[1][-1] != '/':
            invalidProgramUsage()
        return argv[1], argv[2]


# Given a combined Data Map, this method drops all the Counties with bad data
# dictionary(string, dictionary(string, value)) --> void
def dropBadData(combinedDataMap):
    badKeys = []
    for key in combinedDataMap.keys():
        if len(combinedDataMap[key].keys()) != 2 * 2 + 2:
            badKeys.append(key)
            continue
        for column in combinedDataMap[key]:
            if column != "cid" and column != "year":
                try:
                    x = float(combinedDataMap[key][column])
                except:
                    badKeys.append(key)
                    break
    for key in badKeys:
        combinedDataMap.pop(key)
    return


# Given a directory path containing a set of csvDataMap files, this method returns a dictionary that combines the data (inner join)
# string --> dictionary(string, dictionary(string, value))
def combineDataMaps(inputDataDirectory):
    # Create the combined Data Map to be returned
    combinedDataMap = {}

    # Get a list of filepaths to open
    inputDataFilepaths = []
    for year in os.listdir(inputDataDirectory):
        yearFilepath = os.path.join(inputDataDirectory, year)
        for filepath in os.listdir(yearFilepath):
            if filepath.endswith(".csv"):
                inputDataFilepaths.append(os.path.join(yearFilepath, filepath))

    # Add the data to the combined Data Map
    for inputDataFilepath in inputDataFilepaths:
        inputFp = open(inputDataFilepath, "r")
        line = inputFp.readline()
        header = line.split(",")
        line = inputFp.readline()
        while line != "":
            tokens = line.split(",")
            county = tokens[0] + ", " + tokens[1]
            year = int(tokens[-1].strip())
            key = (county, year)
            if key not in combinedDataMap:
                combinedDataMap[key] = {}
                combinedDataMap[key]["cid"] = "\"%s\"" % (county)
                combinedDataMap[key]["year"] = year
            combinedDataMap[key][header[2].strip()] = tokens[2].strip()
            combinedDataMap[key][header[3].strip()] = tokens[3].strip()
            line = inputFp.readline()
        inputFp.close()

    # Drop the bad data
    dropBadData(combinedDataMap)

    # Return the combined Data Map
    return combinedDataMap


# Given a file pointer to write to and a path of a CreateTables.sql file to read from,
# this method writes the Header and INSERT statement to the output file pointer to 
# reflect the structure of the SQL Table created in CreateTables.sql.
# This method returns a list of the columns in the desired order
# fp, string --> string[]
def writeFillTablesHeader(outFP, createTablesSQLFilepath):
    inFP = open(createTablesSQLFilepath, "r")

    beforeColumns = True
    afterColumns = False
    columnsString = ""
    columns = []
    line = inFP.readline()
    while line != "":
        tokens = line.split()
        if beforeColumns:
            if len(tokens) > 0:
                if tokens[0] != "CREATE":
                    outFP.write(line)
                else:
                    outFP.write("INSERT INTO %s\n\t(\n" % (tokens[2]))
                    beforeColumns = False
            else:
                outFP.write(line)
        elif not beforeColumns and not afterColumns:
            if tokens[0] == "PRIMARY" and tokens[1] == "KEY":
                afterColumns = True
            else:
                columnsString += "\t%s,\n" % (tokens[0])
                columns.append(tokens[0])
        else:
            outFP.write("%s\n\t)\nVALUES\n" % (columnsString[:-2]))
            break
            
        line = inFP.readline()

    return columns


# Given a dictionary (representing a single row) mapping SQL Table Columns to values and the order of Columns to be inserted,
# return the tuple to be used in the SQL INSERT statement
# dictionary(string, value) --> string
def getCountyTuple(rowDictionary, orderedColumns):
    countyTuple = "("
    for column in orderedColumns:
        countyTuple += "%s, " % (rowDictionary[column])
    countyTuple = countyTuple[:-2]
    countyTuple += ')'

    return countyTuple


# This program creates a map of the data in the given data filepath and writes the data to
# an SQL INSERT script
# string[] --> int
def main(argv):
    # Check for valid program usage and open needed files
    dataMapDirectory, databaseSourceRoot = checkArgv(argv)
    fillTablesSQLFilepath = databaseSourceRoot + "FillTables.sql"
    outFP = open(fillTablesSQLFilepath, "w")

    # Create a Dictionary that maps (County, Year) to a Dicitionary mapping SQL Columns to Vaules
    counties = combineDataMaps(dataMapDirectory)

    # Write the SQL file header and INSERT statements based on the CreateTables.sql script
    createTablesSQLFilepath = databaseSourceRoot + "CreateTables.sql"
    columns = writeFillTablesHeader(outFP, createTablesSQLFilepath)

    # Fill in the tuples of the SQL Table
    keys = list(counties.keys())
    for key in keys[:-1]:
        keyTuple = getCountyTuple(counties[key], columns)
        outFP.write("\t%s,\n" % (keyTuple))
    keyTuple = getCountyTuple(counties[keys[-1]], columns)
    outFP.write("\t%s;\n" % (keyTuple))

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
# Wesley Reynolds
# CSC - 492


# Library dependencies
import sys
import csv


# Global Constants
NUM_BUCKETS = 256 * 2

stateAbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "AL": "AL",
    "AK": "AK",
    "AZ": "AZ",
    "AR": "AR",
    "CA": "CA",
    "CO": "CO",
    "CT": "CT",
    "DE": "DE",
    "FL": "FL",
    "GA": "GA",
    "HI": "HI",
    "ID": "ID",
    "IL": "IL",
    "IN": "IN",
    "IA": "IA",
    "KS": "KS",
    "KY": "KY",
    "LA": "LA",
    "ME": "ME",
    "MD": "MD",
    "MA": "MA",
    "MI": "MI",
    "MN": "MN",
    "MS": "MS",
    "MO": "MO",
    "MT": "MT",
    "NE": "NE",
    "NV": "NV",
    "NH": "NH",
    "NJ": "NJ",
    "NM": "NM",
    "NY": "NY",
    "NC": "NC",
    "ND": "ND",
    "OH": "OH",
    "OK": "OK",
    "OR": "OR",
    "PA": "PA",
    "RI": "RI",
    "SC": "SC",
    "SD": "SD",
    "TN": "TN",
    "TX": "TX",
    "UT": "UT",
    "VT": "VT",
    "VA": "VA",
    "WA": "WA",
    "WV": "WV",
    "WI": "WI",
    "WY": "WY"
}


# Given a US Census County name, return a US County SVG name
# string --> string
def getCounty(fullCounty):
    if fullCounty == "Baltimore city, Maryland":
        return "Baltimore City,MD"

    tokens = fullCounty.split(",")
    county = ""
    for token in tokens[0].split()[:-1]:
        county += token + " "
    county = county.strip()
    fullState = tokens[1].strip()
    if fullState in stateAbrev:
        state = stateAbrev[tokens[1].strip()]
    else:
        state = ""

    return county + "," + state


# Given a SQL column header, this method exits the program if the CreateTables.SQL does not contain the given column header
# string --> void
def checkDBforSQLCol(sql_col):
    createTablesSQLFilepath = "../../DatabaseSource/CreateTables.sql"
    createTableFp = open(createTablesSQLFilepath, "r")

    line = createTableFp.readline()
    while line != "":
        tokens = line.split()
        if sql_col in tokens:
            return
        line = createTableFp.readline()

    print("\"%s\" is not an existing column in %s" % (sql_col, createTablesSQLFilepath))
    exit(1)


# This method displays the intended program usage and exits the program
# --> exit()
def invalidProgramUsage():
    print("USAGE: censusToDataMap.py DATA_FILEPATH DATA_COLUMN SQL_COLUMN YEAR OUTPUT_FILEPATH")
    print("WHERE: DATA_FILEPATH is filepath of a US Census csv file")
    print("WHERE: DATA_COLUMN is the \'string\' containing the desired column suffix")
    print("WHERE: SQL_COLUMN is the string containing the desired SQL column name")
    print("WHERE: YEAR is the year the data was collected from")
    print("WHERE: OUTPUT_FILEPATH is root directory of the desired csvDataMap file")
    exit(1)


# Given an argument vector, this method checks that program was called correctly.
# If the program is called correctly, the given filepath is returned
# string[] --> string
def checkArgv(argv):
    if len(argv) != 6:
        invalidProgramUsage()
    else:
        return argv[1], argv[2].strip("\'"), argv[3].strip(), argv[4], argv[5]


# Given csv data and a column identifier, this method returns a dictionary that maps
# the states to the index they are at with the column identifier.
# This method only reads the header of the csv data
def getOutputMap(csvData, identifier_col):
    outputMap = {}

    i = 0
    for row in csvData:
        if i < 2:
            if i == 1:
                j = 0
                for col in row:
                    if identifier_col == col:
                        targetCol = j
                    j += 1
        else:
            county = getCounty(row[1])
            outputMap[county] = row[targetCol]
        i += 1

    return outputMap


# Given a dictionary mapping counties to values, this method returns a dictionary
# that maps values to bucket values
# dictionary(string, value) --> dictionary(value, int)
def getBucketsFromValues(outputMap):
    buckets = {}
    values = []
    for i in outputMap.values():
        try:
            values.append(float(i))
        except:
            continue
    values.sort()
    bucketSize = len(values) / NUM_BUCKETS

    for i in range(len(values)):
        bucket = int(i // bucketSize)
        buckets[values[i]] = bucket

    return buckets


# Given a county from the US census, return the county name used in the svg
# string --> string
def svgCounty(county):
    if "Ana" in county and "NM" in county:
        return "Dona Ana,NM"
    if county[-2:] == "AK":
        tokens = county.split(",")
        if len(tokens) > 1 and ("Cens" in tokens[0] or "and" in tokens[0] or "City" in tokens[0]):
            if "Peninsula" in tokens[0]:
                return "Lake and Peninsula,AK"
            else:
                goodCounty = ""
                for token in tokens[0].split()[:-1]:
                    goodCounty += token + " "
                goodCounty = goodCounty.strip()
                return goodCounty + "," + tokens[1]
        else:
            return county
    elif county[-2:] == "VA":
        tokens = county.split(",")
        if tokens[0][-4:] == "city":
            return tokens[0][:-len(" city") + 2] + "," + tokens[1]
        else:
            return county
    else:
        return county


# Given a data filepath, a column identifier, and a row identifier, this method creates a csv file
# that maps each state to the data under the column identifier in the row identifier
def main(argv):
    # Check for valid program usage and open needed files
    dataFilePath, identifier_col, sql_col, year, outputRoot = checkArgv(argv)
    #checkDBforSQLCol(sql_col)
    inputFp = open(dataFilePath, "r")
    outputFp = open("%s/%s/%s.csv" % (outputRoot, year, sql_col), "w")

    # Create a Dictionary that uses the Census csv data to map County to Value
    csvData = csv.reader(inputFp, delimiter=',', quotechar='"')
    outputMap = getOutputMap(csvData, identifier_col)

    # Create a Dictionary that maps Value to Bucket Value
    buckets = getBucketsFromValues(outputMap)

    # Write contents of Dictionary to csv file
    outputFp.write("county,state,%s,%sBucket,year\n" % (sql_col, sql_col))
    for county in outputMap.keys():
        value = outputMap[county]
        try:
            bucket = buckets[float(value)]
            outputFp.write("%s,%s,%s,%s\n" % (svgCounty(county), value, bucket, year))
        except:
            continue

    # Close files and exit program
    inputFp.close()
    outputFp.close()
    return 0


# Driver routine
if __name__ == "__main__":
    print("Program Execution Started")
    if main(sys.argv) == 0:
        print("Program Execution Terminated Successfully")
    else:
        print("Program Execution Terminated Abnormally")

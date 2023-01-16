# Define data source paths
dataRoot="../../ProgramData/CountyData/"
csvDataMapRoot="../Outputs/CsvDataMaps/"
log="../Outputs/Logs/censusToDataMap.out"

# Function that creates all of the csvDataMaps for a given column of data
writeCsvDataMaps () {
    for yearPath in $dataRoot*
    do
        year=$(basename $yearPath)
        for dataSourcePath in $yearPath/*$1
        do
            python ../Python/censusToDataMap.py $dataSourcePath "'$2'" $3 $year $csvDataMapRoot > $log
        done
    done
}

# Include DP04 Data
dataFileExtension=".DP04-Data.csv"
targetColName="Estimate!!VALUE!!Owner-occupied units!!Median (dollars)"
sqlColName="medianHomeValue"
writeCsvDataMaps "$dataFileExtension" "$targetColName" "$sqlColName"

# Include S1901 Data
dataFileExtension=".S1901-Data.csv"
targetColName="Estimate!!Households!!Median income (dollars)"
sqlColName="medianHouseholdIncome "
writeCsvDataMaps "$dataFileExtension" "$targetColName" "$sqlColName"

# Report that the process has finished
echo "Created csv Data Maps."
# Define data source paths
csvDataMapRoot="../Outputs/CsvDataMaps/"
databaseSourceRoot="../../DatabaseSource/"
log="../Outputs/Logs/dataMapsToSQL.out"

# Create csvDataMaps from the given US Census data
bash censusToDataMaps.sh
# Put the data in the csvDataMaps into the SQL DB
python ../Python/dataMapsToSQL.py $csvDataMapRoot $databaseSourceRoot > $log

# Report that the process has finished
echo "Created the FillTables.sql script."
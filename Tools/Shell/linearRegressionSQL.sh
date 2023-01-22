# Define data source paths
databaseSourceRoot="../../DatabaseSource/"
log="../Outputs/Logs/linearRegressionSQL.out"

# Use the data in the SQL DB to predict future year's data
python ../Python/linearRegressionSQL.py $databaseSourceRoot > $log

# Report that the process has finished
echo "Created the LinearRegression.sql script."
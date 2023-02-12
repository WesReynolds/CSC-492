# Define data source paths
log="../Outputs/Logs/writeHistoryPNGs.out"
csvDataMapRoot="../Outputs/CsvDataMaps/"
outputDir="../../WebApp/HistoryImages/"

# Create the history images for each ColumnName
for columnNamePath in $csvDataMapRoot/2021/*
do
    columnName=$(basename $columnNamePath)
    columnName=${columnName%.*}
    python ../Python/writeHistoryPNGs.py $columnName $outputDir #> $log
    echo "$columnName"
done

# Report that the process has finished
echo "Created the history images."
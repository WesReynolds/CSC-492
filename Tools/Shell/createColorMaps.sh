# Define data source paths
countiesSVG="../../ProgramData/SvgMaps/counties.svg"
csvDataMapRoot="../Outputs/CsvDataMaps/"
svgRoot="../Outputs/SVGs/"
colorMapRoot="../../WebApp/ColorMaps/"
noColorMapRoot="../../WebApp/NoColorMaps/"
log1="../Outputs/Logs/writeColorHTML.out"
log2="../Outputs/Logs/writeColorSVG.out"
log3="../Outputs/Logs/replaceSVGInHTML.out"

# Create the no color map html files, then update the svgs in them accordingly
for columnNamePath in $csvDataMapRoot/2021/*
do
    columnName=$(basename $columnNamePath)
    columnName=${columnName%.*}
    for yearPath in $colorMapRoot*
    do
        year=$(basename $yearPath)
        python ../Python/writeColorHTML.py $noColorMapRoot/index.html $year $columnName $colorMapRoot$year/$columnName.html > $log1
        python ../Python/writeColorSVG.py $countiesSVG $year $columnName $svgRoot$year/$columnName.svg > $log2
        python ../Python/replaceSVGInHTML.py $colorMapRoot$year/$columnName.html $colorMapRoot$year/$columnName.html $svgRoot$year/$columnName.svg > $log3
    done
done

# Report that the process has finished
echo "Created the colored maps."
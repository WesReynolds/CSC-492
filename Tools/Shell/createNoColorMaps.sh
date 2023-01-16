# Define data source paths
countiesSVG="../../ProgramData/SvgMaps/counties.svg"
svgRoot="../Outputs/SVGs/"
noColorMapRoot="../../WebApp/NoColorMaps/"
log1="../Outputs/Logs/createNoColorHTML.out"
log2="../Outputs/Logs/writeNoColorSVG.out"
log3="../Outputs/Logs/replaceSVGInHTML.out"

# Create the no color maps
for yearPath in $svgRoot*
do
    year=$(basename $yearPath)
    python ../Python/writeNoColorHTML.py $noColorMapRoot/index.html $year $noColorMapRoot$year.html > $log1
    python ../Python/writeNoColorSVG.py $countiesSVG $year $svgRoot$year/NoColor.svg > $log2
    python ../Python/replaceSVGInHTML.py $noColorMapRoot$year.html $noColorMapRoot$year.html $svgRoot$year/NoColor.svg > $log3
done

# Report that the process has finished
echo "Created the no color maps."
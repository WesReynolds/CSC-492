# Start using the "seniorproject" Schema
USE seniorproject;

/*
# View the Counties Table
SELECT * FROM Counties;
*/

SELECT * FROM Counties WHERE year = 2024;

SELECT * FROM Counties WHERE cid = "Santa Fe, NM";

SELECT cid, AVG(population) FROM Counties GROUP BY cid;

SELECT sexRatioBucket FROM Counties ORDER BY sexRatioBucket DESC;

# View Bucket 0
SELECT AVG(percentHighSchool) FROM Counties
WHERE percentHighSchoolBucket >= 0 AND percentHighSchoolBucket <= 2;

# View Bucket 25
SELECT AVG(percentHighSchool) FROM Counties
WHERE percentHighSchoolBucket >= 125 AND percentHighSchoolBucket <= 129;

# View Bucket 50
SELECT AVG(percentHighSchool) FROM Counties
WHERE percentHighSchoolBucket >= 253 AND percentHighSchoolBucket <= 257;

# View Bucket 75
SELECT AVG(percentHighSchool) FROM Counties
WHERE percentHighSchoolBucket >= 381 AND percentHighSchoolBucket <= 385;

# View Bucket 100
SELECT AVG(percentHighSchool) FROM Counties
WHERE percentHighSchoolBucket >= 509 AND percentHighSchoolBucket <= 511;

/*
# View the 5 buckets in the key
SELECT cid, medianHomeValue, medianHomeValueBucket
FROM COUNTIES
WHERE medianHomeValueBucket IN (0, 127, 258, 384, 511)
ORDER BY medianHomeValueBucket ASC, medianHomeValue ASC;

# Show the contents of States in descending order of percent receiving SNAP services
#SELECT * FROM States ORDER BY percentSNAP DESC;

# Show the contents of States in descending order of percent receiving Average Income
#SELECT * FROM States ORDER BY avgIncome DESC;

# Show the contents of States in descending order of Sex Ratio (higher = more men)
#SELECT * FROM States ORDER BY sexRatio DESC;

# Show the contents of Counties in descending order of Median Home Value
SELECT * FROM Counties ORDER BY percentHighSchool DESC;

# View Santa Fe
SELECT * FROM Counties WHERE cid = "Santa Fe, NM";

# Show the contents of Counties in descending order of percent of people 16+ that are employed
SELECT * FROM Counties ORDER BY percent16OverEmployed DESC;

# Select a specific county
SELECT * FROM Counties
WHERE cid = "Lassen, CA";

# Get the statistics for Median Home Value
SELECT AVG(medianHomeValue), MAX(medianHomeValue), MIN(medianHomeValue) FROM Counties;

# Show the contents of Counties in descending order of Median Household Income
SELECT * FROM Counties ORDER BY medianHouseholdIncome DESC;

# Get the statistics for Median Household Income
SELECT AVG(medianHouseholdIncome), MAX(medianHouseholdIncome), MIN(medianHouseholdIncome) FROM Counties;

# Get the number of entries in the table
SELECT COUNT(*) FROM Counties;

# View the Counties Table
SELECT * FROM Counties ORDER BY percentNoHighSchool DESC;

# Get Average value of Column in Counties Table
SELECT AVG(medianHomeValue) FROM Counties;

# Get STD Dev of Column in Counties Table
SELECT FORMAT(stddev_samp(medianHomeValue), 2)
FROM (SELECT * FROM Counties) t;
*/

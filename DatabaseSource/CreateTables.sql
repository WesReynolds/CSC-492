# Start using the "seniorproject" Schema
USE seniorproject;

# Define the Counties Table
CREATE TABLE Counties (
	cid VARCHAR(50),
    year INT,
    medianHomeValue INT,
    medianHomeValueBucket INT,
    medianHouseholdIncome INT,
    medianHouseholdIncomeBucket INT,
    population INT,
    populationBucket INT,
    percentHighSchool FLOAT,
    percentHighSchoolBucket INT,
    percentCollege FLOAT,
    percentCollegeBucket INT,
    PRIMARY KEY (cid, year)
);

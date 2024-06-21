# Data-Challenge-2-Group-1

Welcome to the repository for the project of Group 1 in the academic year 2024-2025 for the course Data Challenge 2.

## Data downloads
To succesfully run this code, a few data sets need to be downloaded first.
The first of these is the PAS data on ward level for the year of 2019-2020, which we do not have a link for.
Make sure this file has the name: 'PAS_ward_level_FY_19_20.csv'

The second is one that has geographical coordinates of the boroughs in London, 
found under the name 'London-wards-2018.zip at: https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london

And the last data set we used, but is not necessary for the code we used for our results,
is about deprivation in local wards, to be downloaded after locking the reference period (2019)
at: https://opendatacommunities.org/resource?uri=http%3A%2F%2Fopendatacommunities.org%2Fdata%2Fsocietal-wellbeing%2Fimd2019%2Findices

## How to run the files
After downloading all data, first run the file called 'preprocessing.py', in order to get a preprocessed version of the PAS data.

Now to get our regression results run the 'Multivariate Regression.R' and 'Multivariate Regression Encoded.R' files, 
for our clustering on the highest qualification of people within a borough, run the 'clustering_based_on_education_index.ipynb' file 
and for the leftover visualizations look at 'visualizations.ipynb' and 'visualizations.py'.
The files that were not named were used to look into directions we decided not to pursue during this course, or did not yield useful results.
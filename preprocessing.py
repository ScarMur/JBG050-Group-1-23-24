#Download packages
import pandas as pd
from pathlib import Path  
import geopandas as gpd

#Open the data as a dataframe, be sure it has this name and is in the data folder.
df = pd.read_csv('PAS_ward_level_FY_19_20.csv')

#Now we aggregate the education levels to be the same where they are equivalent.
df.NQ146.unique()
replacement_dict = {'BTEC Level 1': 'O-levels/CSE/GCSEs','BTEC level 2':'O-levels/CSE/GCSEs','BTEC level 3':'A-levels',
                    'NVQ/GNVQ':'apprenticeship', 'Trade apprenticeship':'apprenticeship', 'ONC, OND or City and Guilds':'A-levels'
                    }
df = df.replace({'NQ146':replacement_dict})
#We also string some unnecessary white spaces
df['ward_unique'] = df['ward_unique'].str.strip()


#We now seperate the column ward_unique into the ward, which we use to replace the ward_n column which is the same data
#and we also create a borough column
df[['ward_n','borough']] = df['ward_unique'].str.split('-', expand=True)
#Remove random white spaces.
df['ward_n'] = df['ward_n'].str.strip()
df['borough'] = df['borough'].str.strip()
#Remove the dots in the ward names.
df['ward_n'] = df['ward_n'].str.replace('.','')

#We now make sure the boroughs are spelled correctly by using a dataset that has the boroughs spelled completely and correctly and
#then changing them depending on the ward.

#So we first get the other dataset:
shapefile_path = "London-wards/London_Ward.shp" 
gdf = gpd.read_file(shapefile_path, )
gdf = gdf.rename(columns={'NAME': 'ward_n','DISTRICT':'borough'})
#Remove the rows that are about the City of London
gdf = gdf.drop(gdf[gdf['borough'] == 'City and County of the City of London'].index)

#Remove the dots in the ward names.
gdf['ward_n'] = gdf['ward_n'].str.replace('.','')

#Fixing a difference in spelling
gdf = gdf.replace({'Shirly South':'Shirley South'})

#Then we fix the incorrect ward names in the PAS dataset
spatial_wards = list(gdf.ward_n.unique())
pas_wards = list(df.ward_n.unique())
pas_wards.sort()
spatial_wards.sort()
non_overlap_pas = [x for x in pas_wards if x not in set(spatial_wards)]

pas_wards_dict = {'Camden Town with Primrose H': 'Camden Town with Primrose Hill', 'Chelsfield and Pratts Botto': 'Chelsfield and Pratts Bottom','Crystal Palace & Upper Norw':
                  'Crystal Palace & Upper Norwood','Ham, Petersham and Richmond': 'Ham, Petersham and Richmond Riverside',
                  'London Bridge & West Bermon': 'London Bridge & West Bermondsey'}

for ward in non_overlap_pas:
    mask = df['ward_n'] == ward
    df.loc[mask, 'ward_n'] = pas_wards_dict[ward]

#Make a dictionary that for each ward looks at in which boroughs it appears and then sort it by amount of boroughs in which it appears.
wards_dict = {}
for row in range(len(gdf)):
    if gdf.loc[row]['ward_n'] not in wards_dict.keys():
        wards_dict[gdf.loc[row]['ward_n']] = [gdf.loc[row]['borough']]
    elif gdf.loc[row]['borough'] not in wards_dict[gdf.loc[row]['ward_n']]:
        wards_dict[gdf.loc[row]['ward_n']] += [gdf.loc[row]['borough']]


#Then we correct the wrongly spelled boroughs:
#Fix the borough names issues in the PAS data.
for ward in df.ward_n.unique():

    #If this ward only has 1 borough, replace the borough column with said borough.
    if len(wards_dict[ward]) == 1:

        #Find the lines in which this ward occurs
        mask = df['ward_n'] == ward

        df.loc[mask, 'borough'] = wards_dict[ward][0]

    #Else, see with which of the options in the dictionary the first value in the dataframe coincides and use that borough.
    else:
        #Find the different boroughs we can have
        borough_1 = wards_dict[ward][0]
        borough_2 = wards_dict[ward][1]

        #For the first one, find the rows with this ward and this borough, and replace them with the full borough name
        mask = (df['ward_n'] == ward) & (df['borough'].str.startswith(borough_1[0]))
        df.loc[mask, 'borough'] = borough_1

        #Do the same with the other borough
        mask = (df['ward_n'] == ward) & (df['borough'].str.startswith(borough_2[0]))
        df.loc[mask, 'borough'] = borough_2



#Make the filepath to save the changed data
filepath = Path('preprocessed.csv')
#Save the changed dataframe as a csv file.  
df.to_csv(filepath)
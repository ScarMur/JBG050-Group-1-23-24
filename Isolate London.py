import pandas as pd
from io import StringIO


# Path to the dataset using a raw string to avoid unicode escape errors
file_path = r'societal-wellbeing_imd2019_indices.csv'

# Read the entire file into a Python string
with open(file_path, 'r') as file:
    data = file.read()

# Split each line at the first comma and join back with the rest of the line
processed_data = '\n'.join([','.join(line.split(',')[1:]) for line in data.split('\n')])

# Convert the processed data string back to a DataFrame
data_df = pd.read_csv(StringIO(processed_data))

# Optionally, rename the first column to 'Reference area' if it represents areas
data_df.columns = ['Reference area'] + list(data_df.columns[1:])

# List of London boroughs to filter the dataset
london_boroughs = [
    "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley",
    "Camden", "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
    "Hammersmith and Fulham", "Haringey", "Harrow", "Havering",
    "Hillingdon", "Hounslow", "Islington", "Kensington and Chelsea",
    "Kingston upon Thames", "Lambeth", "Lewisham", "Merton", "Newham",
    "Redbridge", "Richmond upon Thames", "Southwark", "Sutton",
    "Tower Hamlets", "Waltham Forest", "Wandsworth", "Westminster", "City of London"
]

# Regex pattern to match any of the London boroughs in the 'Reference area' column
pattern = '|'.join(london_boroughs)

# Filter data to include only London boroughs
data_london = data_df[data_df['Reference area'].str.contains(pattern, na=False)]

# Display the first 10 rows of the filtered data
print(data_london.head(10))
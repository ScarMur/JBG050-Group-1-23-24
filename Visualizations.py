import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Open the data as a dataframe, be sure it has this name and is in the data folder.
df = pd.read_csv('PAS_ward_level_FY_19_20.csv')

#Now we aggregate the education levels to be the same where they are equivalent.
df.NQ146.unique()
replacement_dict = {'BTEC Level 1': 'O-levels/CSE/GCSEs','BTEC level 2':'O-levels/CSE/GCSEs','BTEC level 3':'A-levels',
                    'NVQ/GNVQ':'apprenticeship', 'Trade apprenticeship':'Apprenticeship', 'ONC, OND or City and Guilds':'A-levels'
                    }
df = df.replace({'NQ146':replacement_dict})

# Filter the df
include_levels = ['Post-graduate degree or qualification', 'University Degree (Bachelor degree)', 'HNC or HND/BTEC level 4', 'Apprenticeship']
exclude_answers = ['None/nothing', 'Not asked', 'None / nothing']

df_filtered = df[df['NQ146'].isin(include_levels)]

# Melt the df to combine answers into one column, filter out excluded answers
df_melted_local = df_filtered.melt(id_vars='NQ146', value_vars=['NPQ135A', 'NPQ135B', 'NPQ135C'], var_name='priority', value_name='answer')

df_melted_local = df_melted_local[~df_melted_local['answer'].isin(exclude_answers)]

# Count occurrences of each answer for each education level
local_counts = df_melted_local.groupby(['answer', 'NQ146']).size().unstack(fill_value=0)

# Filter out answers with total counts below a certain threshold
threshold = 250
local_filtered_counts = local_counts[local_counts.sum(axis=1) >= threshold]

# Sort the answers in descending order based on total count

local_filtered_counts['total'] = local_filtered_counts.sum(axis=1)
local_filtered_counts = local_filtered_counts.sort_values(by='total', ascending=False).drop(columns='total')

# Plotting
fig, ax = plt.subplots(figsize=(10,6))

index = np.arange(len(local_filtered_counts))

colors = ['#648FFF', '#DC267F', '#FE6100', '#FFB000']

bottom = None
for i, education_level in enumerate(local_filtered_counts.columns):
    if bottom is None:
        bottom = local_filtered_counts[education_level]
        ax.bar(index, local_filtered_counts[education_level], label=education_level, color=colors[i])
    else:
        ax.bar(index, local_filtered_counts[education_level], bottom=bottom, label=education_level, color=colors[i])
        bottom += local_filtered_counts[education_level]

ax.set_xlabel('Concern')
ax.set_ylabel('Count')
ax.set_title('Priorities by Education Level, Local')
ax.set_xticks(index)
ax.set_xticklabels(local_filtered_counts.index)
ax.legend(title='Education Level')

plt.xticks(rotation=20, ha='right', fontsize=10)
plt.tight_layout()

plt.show()

# Melt the df to combine answers into one column, global, filter out excluded answers
df_melted_global = df_filtered.melt(id_vars='NQ146', value_vars=['NNQ135A_newA', 'NNQ135A_newB', 'NNQ135A_newC'], var_name='priority', value_name='answer')

df_melted_global = df_melted_global[~df_melted_global['answer'].isin(exclude_answers)]
# Count occurrences of each answer for each education level
global_counts = df_melted_global.groupby(['answer', 'NQ146']).size().unstack(fill_value=0)

# Filter out answers with total counts below a certain threshold
threshold = 250
global_filtered_counts = global_counts[global_counts.sum(axis=1) >= threshold]

# Sort the answers in descending order based on total count

global_filtered_counts['total'] = global_filtered_counts.sum(axis=1)
global_filtered_counts = global_filtered_counts.sort_values(by='total', ascending=False).drop(columns='total')

# Plotting
fig, ax = plt.subplots(figsize=(10,6))

index = np.arange(len(global_filtered_counts))

bottom = None
for i, education_level in enumerate(global_filtered_counts.columns):
    if bottom is None:
        bottom = global_filtered_counts[education_level]
        ax.bar(index, global_filtered_counts[education_level], label=education_level, color=colors[i])
    else:
        ax.bar(index, global_filtered_counts[education_level], bottom=bottom, label=education_level, color=colors[i])
        bottom += global_filtered_counts[education_level]

ax.set_xlabel('Concern')
ax.set_ylabel('Count')
ax.set_title('Priorities by Education Level, Global')
ax.set_xticks(index)
ax.set_xticklabels(global_filtered_counts.index)
ax.legend(title='Education Level')

plt.xticks(rotation=20, ha='right', fontsize=10)

# Dictionary to map original labels to shortened labels
global_label_map = {
    'Gun/knife crime': 'Gun/knife crime',
    'Terrorism': 'Terrorism',
    'Drugs and drug-related crime': 'Drugs and drug-related crime',
    'Gangs and gang-related crimes': 'Gangs and gang-related crimes',
    'Anti-social behaviour (ASB)': 'Anti-social behaviour (ASB)',
    'Traffic/road related issues': 'Traffic/road related issues',
    'Hate crime (e.g. racially or religiously motivated crimes, homophobic crimes etc)': 'Hate crime'  # Example of shortening a specific label
}

# Get current x-tick labels and update them based on the dictionary
current_labels = [item.get_text() for item in ax.get_xticklabels()]
new_labels = [global_label_map.get(label, label) for label in current_labels]
ax.set_xticklabels(new_labels)

plt.tight_layout()

plt.show()

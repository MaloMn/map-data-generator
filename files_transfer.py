import pathlib
import pandas as pd
from shutil import copyfile
from pathlib import Path

current_folder = Path.cwd()
destination_folder = Path(str(current_folder).replace("map_data_generator", "map")) / 'data'
print("Copying data: {} --> {}\n".format(current_folder, destination_folder))

# Gathering data
data = pd.read_csv("anki_data/cleaned_data.csv")

# Filtering the data to keep wanted lines and header
# CUSTOM CODE
# short_list = ['united_states_of_america', 'france', 'china', 'russia', 'canada', 'brazil']
# transfer_choice = data.apply(lambda x: x.short in short_list, axis=1)
transfer_choice = data.apply(lambda x: 'Sovereign_State' in x.tags, axis=1)

data = data[transfer_choice]
data = data.drop(data.columns[0], axis=1)
data = data.reset_index()
del data['index']

# Save this array in the dest_folder
data.to_csv(destination_folder / 'data.csv', sep=',')
print(data.head())

# Getting the shorts of chosen areas
shorts = list(data.short)

# Copy the polygons, pinpoints, flags
for f in ['pinpoints', 'polygons_collision', 'polygons_display', 'flags']:
    for s in shorts:
        name = f + '/' + s
        name = name + '.json' if f != 'flags' else name + '.png'

        try:
            copyfile(current_folder / name, destination_folder / name)
        except FileNotFoundError:
            print("Could not find ", current_folder / name)

    print("Copied {} {}".format(len(shorts), f))

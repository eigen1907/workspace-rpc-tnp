import json
import re

# File paths
txt_file_path = './roll-blacklist-2022.txt'
json_file_path = './roll-blacklist-2022.json'

# Read the txt file and extract the blacklist items
with open(txt_file_path, 'r') as txt_file:
    lines = txt_file.readlines()

# Function to clean the RB substring
def clean_rb(item):
    # Replace RB@++ with RB@+, and RB@-- with RB@-
    item = re.sub(r'RB(\d+)\+\+', r'RB\1+', item)
    item = re.sub(r'RB(\d+)\-\-', r'RB\1-', item)
    # Remove any remaining + or - after RB@
    item = re.sub(r'RB(\d+)[+-]', r'RB\1', item)
    return item

# Extract and clean the necessary data (second column from each line)
blacklist_items = {clean_rb(line.split()[1]) for line in lines}  # Using a set to remove duplicates

# Convert set back to list for sorting
blacklist_items = list(blacklist_items)

# Sort the items
blacklist_items.sort()

# Write the data to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(blacklist_items, json_file, indent=4)

print(f"Converted {txt_file_path} to {json_file_path}")
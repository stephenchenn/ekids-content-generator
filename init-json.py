import json
import copy
import datetime

import sys

if len(sys.argv) <= 1:
    print('Please provide the year')
    sys.exit()
else:
    # The first argument after the script name
    year = int(sys.argv[1])


def get_sundays_month(year, month):
    # Create a date object for the first day of the month
    first_day = datetime.date(year, month, 1)
    # Find the first Sunday in the month
    first_sunday = first_day + datetime.timedelta(days=(6 - first_day.weekday()) % 7)
    # Generate all Sundays in the month
    sundays = []
    current_day = first_sunday
    while current_day.month == month:
        sundays.append(current_day)
        current_day += datetime.timedelta(days=7)
    return sundays

# List of month names
months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

# Create default attributes for each Sunday
default_attributes = {
    "material_url": "",
    "video_url": ""
}

types = ["EKIDS1", "EKIDS2"]

# Create the Python dictionary with the desired structure
data = {
    year: {type: {} for type in types}
}

# Loop through each month and populate the data dictionary
for month_index, type in enumerate(types, start=1):
    for month_index, key1 in enumerate(months, start=1):
        # Get all Sundays in the current month
        sundays = get_sundays_month(year, month_index)
        # Format the Sundays as strings
        formatted_sundays = [sunday.strftime("%Y-%m-%d") for sunday in sundays]
        
        # Initialize the month key in the data dictionary
        data[year][type][key1] = {}
        
        # Populate each Sunday with default attributes
        for sunday in formatted_sundays:
            data[year][type][key1][sunday] = copy.deepcopy(default_attributes)

# Write the dictionary to a JSON file
# json.dump Serializes a Python object into a JSON formatted stream

filename=f"{year}-links.json"

with open(filename, 'w') as file:
    json.dump(data, file, indent=4)

print("Generated JSON Skeleton for links")
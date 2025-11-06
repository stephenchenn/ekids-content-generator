import dropbox
import re
import json
import sys

if len(sys.argv) <= 1:
    print('Please provide the year')
    sys.exit()
else:
    # The first argument after the script name
    year = sys.argv[1]

filename=f"{year}-links.json"
# Load the JSON data from the file
with open(filename, 'r') as file:
    data = json.load(file)

# Function to recursively list all subfolders
def find_deepest_subfolders(dbx, path):
    # Get the list of entries in the folder
    response = dbx.files_list_folder(path)

    # A list to keep track of the subfolders within the current folder
    subfolders = []

    # A flag to determine if the current folder has any subfolders
    has_subfolders = False

    # Check each entry to identify subfolders
    for entry in response.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            has_subfolders = True
            # Recursively find subfolders within this folder
            deeper_subfolders = find_deepest_subfolders(dbx, entry.path_display)
            subfolders.extend(deeper_subfolders)

    # If the current folder doesn't contain any subfolders, it must be the deepest
    if not has_subfolders:
        print(f"found subfolder: {path}\n")
        subfolders.append(path)

    # Handle pagination if needed
    while response.has_more:
        response = dbx.files_list_folder_continue(response.cursor)
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                has_subfolders = True
                deeper_subfolders = find_deepest_subfolders(dbx, entry.path_display)
                subfolders.extend(deeper_subfolders)

    return subfolders

# Your Dropbox access token
ACCESS_TOKEN = sys.argv[2]

# Path to the folder in Dropbox
FOLDER_PATH = f"/church-ekids-program/{year}"

# Initialize a Dropbox object
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# List all subfolders recursively
all_subfolders = find_deepest_subfolders(dbx, FOLDER_PATH)

# Regular expression pattern
pattern = r'^/[^/]+/(\d{4})/([^/]+)/([^/]+)/([^/]+)/([^/]+)$'

for subfolder in all_subfolders:
    # Create a shared link for the folder
    try:
        # First, try to create the shared link
        shared_link = dbx.sharing_create_shared_link_with_settings(subfolder)
    except dropbox.exceptions.ApiError as e:
        if (e.error.is_shared_link_already_exists()):
            # If the shared link already exists, retrieve it
            print('shared link already exists, existing link:')
            shared_link = dbx.sharing_list_shared_links(path=subfolder).links[0]
        else:
            raise

    # Perform regex matching
    # print(subfolder)

    match = re.match(pattern, subfolder)
    if match:
        year = match.group(1)
        level = match.group(2)
        month = match.group(3)
        date = match.group(4)
        materialOrVideo = match.group(5)
    else:
        print("No match found.")
        sys.exit()

    if (materialOrVideo == 'Materials'):
        type="material_url"
    else:
        type="video_url"

    data[year][level][month][date][type]=shared_link.url

    # Output the URL of the shared link
    print(f"link for {level} {month} {date} {type}:\n {shared_link.url}\n")

with open(filename, 'w') as file:
    json.dump(data, file, indent=4)
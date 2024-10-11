import datetime
import dropbox
import sys

if len(sys.argv) <= 1:
    print('Please provide the year')
    sys.exit()
else:
    # The first argument after the script name
    year = sys.argv[1]
    

# Your Dropbox access token
ACCESS_TOKEN = sys.argv[2]
FOLDER_PATH = '/church-ekids-program/' + year

dbx = dropbox.Dropbox(ACCESS_TOKEN)

def get_sundays(year):
    # January 1st of the given year
    first_day = datetime.date(year, 1, 1)
    
    # Find the first Sunday of the year
    first_sunday = first_day + datetime.timedelta(days=(6 - first_day.weekday()))
    
    # Initialize an empty list to hold the Sundays
    sundays = []
    
    # Iterate over the year and add a week (7 days) to get each Sunday
    current_sunday = first_sunday
    while current_sunday.year == year:
        sundays.append(current_sunday)
        current_sunday += datetime.timedelta(days=7)
    
    return sundays

def get_sundays_month(year, month):
    sundays = get_sundays(year)
    # Filter for Sundays that are in January
    january_sundays = [sunday for sunday in sundays if sunday.month == month]
    return january_sundays

# create folder for the year
dbx.files_create_folder_v2(FOLDER_PATH)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ekids = ["EKIDS1", "EKIDS2"]

for ekid in ekids:
    print(f"creating folders for {ekid}...\n")
    current_folder = FOLDER_PATH + "/" + ekid

    for i in range(1, 13):
        january_sundays = get_sundays_month(int(year), i)
        month = months[i - 1]
        dbx.files_create_folder_v2(current_folder + "/" + month)
        print(f"creating folders for {month}...")
        for sunday in january_sundays:
            formatted_sunday = sunday.strftime("%Y-%m-%d")  # You can customize the format
            dbx.files_create_folder_v2(current_folder + "/" + month + "/" + formatted_sunday)

            dbx.files_create_folder_v2(current_folder + "/" + month + "/" + formatted_sunday + "/" + "Materials")
            dbx.files_create_folder_v2(current_folder + "/" + month + "/" + formatted_sunday + "/" + "Videos")
            print(f"created folder for {formatted_sunday}")
        print('\n')

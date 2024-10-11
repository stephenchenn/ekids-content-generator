import json
from datetime import datetime

import sys

if len(sys.argv) <= 1:
    print('Please provide the year')
    sys.exit()
else:
    # The first argument after the script name
    year = sys.argv[1]

filename=f"{year}-links.json"

# Read the JSON file
with open(filename, 'r') as f:
    data = json.load(f)

# Create an HTML string
html_content = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title></title>
    <style>
      /* Parent container taking full width */
      .split-container {
        display: flex;
        justify-content: center;
        align-items: center;
      }

      /* Children are flex items with equal width */
      .split-half {
        text-align: center; /* Center-align text horizontally */
        display: block;
        float: left;
        width: 50%;
        font-family: proxima-nova;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
      }

      a {
        color: rgb(61, 153, 145);
      }
    </style>
  </head>
  <body>
    <div class="split-container">
"""

# Traverse the JSON data
for year, ekids_data in data.items():
    
    for ekids, months in ekids_data.items():
        
        title=''
        if ekids=='EKIDS1':
            title='EKids 1 (2-6 Years Old)'
        else:
            title='Ekids 2 (7-12 years Old)'

        html_content += f'<div class="split-half"><h2>{title}</h2><br>'
        for month, dates in months.items():
            for date, urls in dates.items():
                material_url = urls.get("material_url", "")
                video_url = urls.get("video_url", "")

                # Parse the input date string into a datetime object
                dt = datetime.strptime(date, '%Y-%m-%d')
                output_date = f"{dt.day} {dt.strftime('%b')}"

                html_content += f'<h3>{output_date} | '
                html_content += f'<a href="{video_url}">Video Link</a> | \n'
                html_content += f'<a href="{material_url}">Material</a></h3>\n'
        html_content += '</div>'

# Close the HTML tags
html_content += """
    </div>
  </body>
</html>
"""

# Write the HTML content to an HTML file
with open('links.html', 'w') as f:
    f.write(html_content)

print("HTML file created successfully!")

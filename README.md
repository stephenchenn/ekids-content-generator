to renew access token, go to https://www.dropbox.com/developers/apps/info/df49zavmtwkklcu#settings and click 'Generate access token'

To generate, run:
    ./run.sh

it goes through the following steps:
    1. create.py <year> <token> creates the dropbox folders
    2. init-json.py <year> generates the skeleton json to hold the links to the folders
    3. shared-links-gen.py <year> <token> creates the links and populate them in the skeleton json
    4. html-gen.py <year> uses the link json to create the html to be pasted into squarespace code element

ensure the dropbox is cleared for that year before running it
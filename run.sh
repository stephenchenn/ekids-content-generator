#!/bin/bash

echo -n "Enter the year to generate: "
read year
echo -n "Enter the dropbox access token: "
read token

echo "Generating Ekids Content for year $year!"

echo -e "\n***Creating folders in Dropbox***\n"
python3 create.py $year $token

echo -e "\n***Creating JSON Skeleton to hold links to folders***\n"
python3 init-json.py $year

echo -e "\n***Populating JSON with shared links view only***\n"
python3 shared-links-gen.py $year $token

echo -e "\n***Generating HTML using links***\n"
python3 html-gen.py $year

echo -e "\n***DONE***\n"
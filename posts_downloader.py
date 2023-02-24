# a script to download posts from the website, and save them to a local file 
# for further processing

import requests
import csv
from os.path import exists

# get the URL from the user
print("START: Downloading challenge posts...");
downloaded = 0
skipped = 0
with open('data/challenge_links.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    for week, link in reader:
        filename = "data/challenge_"+week+".html"
        if( not exists(filename) ):
            print("  + Downloading... "+filename+" from "+link)
            r = requests.get(link)
            if( r.status_code != 200 ):
                print("    ! ERROR: "+r.status_code+" - "+r.reason)
                continue
            html = r.text
            with open(filename, "w") as fp:
                fp.write(html)
            downloaded += 1
        else:
            print("  - File "+filename+" already exists. Skipping...")
            skipped += 1

print("DONE: Downloaded "+str(downloaded)+" files, skipped "+str(skipped)+" files.")





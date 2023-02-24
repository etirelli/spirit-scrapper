from bs4 import BeautifulSoup
import re
import csv

def parsePage( html ):
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # get the data from the HTML
    data = soup.find("div", attrs={"data-test-id": "post-content"})
    if( data == None ):
        print("ERROR: could not parse post content")
        print("----------------------------------")
        print(html)
        exit(1)
    post = data.contents[4].text.strip()

    raw_links = data.contents[4].find_all("a", string=re.compile(r'Week (\d+)'))
    print("Parsed links: "+str(len(raw_links)))
    print("Writing to file...")

    with open('data/challenge_links.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for l in raw_links:
            writer.writerow( [l.text, l['href']] )

    print("Done!")

# get the URL from the user
with open("challenge_100.html") as fp:
    html = fp.read()

parsePage(html)
# a script to scrape data from a website by its URL
# and save it to a CSV file for further analysis

import requests
from bs4 import BeautifulSoup
import re
import os
import csv

class Challenge:
    def __init__(self, title=None, expansionSpirits=None, expansionBoardSetup=None, expansionAdversary=None, 
                 expansionScenario=None, baseSpirits=None, baseBoardSetup=None, baseAdversary=None, baseScenario=None):
        self.title = title
        self.expansionSpirits = expansionSpirits
        self.expansionBoardSetup = expansionBoardSetup
        self.expansionAdversary = expansionAdversary
        self.expansionScenario = expansionScenario
        self.baseSpirits = baseSpirits
        self.baseBoardSetup = baseBoardSetup
        self.baseAdversary = baseAdversary
        self.baseScenario = baseScenario

    def __str__(self):
        return "CHALLENGE: " + self.title + "\n" +\
                "EXPANSION CONTENT:\n" + \
                "Spirits: " + str(self.expansionSpirits) + "\n" + \
                "Board Setup: " + str(self.expansionBoardSetup) + "\n" + \
                "Adversary: " + str(self.expansionAdversary) + "\n" + \
                "Scenario: " + str(self.expansionScenario) + "\n" + \
                "--------------------------------\n" + \
                "BASE GAME CONTENT:\n" + \
                "Spirits: " + str(self.baseSpirits) + "\n" + \
                "Board Setup: " + str(self.baseBoardSetup) + "\n" + \
                "Adversary: " + str(self.baseAdversary) + "\n" + \
                "Scenario: " + str(self.baseScenario) + "\n"

def parseSpirits( text ):
    #return a list of tuples (spirit, aspect, starting_board)
    spiritRE = re.compile(r'([\w|\s|\']+?)\s*(?:\((.*?)\))?\s+on\s+board\s+([E\.|W\.|SW\.|NW\.|NE\.|SE\.|A-F])')
    return spiritRE.findall(text)

def parseBoard( text ):
    #return the board setup to use in the challenge
    boardRE = re.compile(r'Board Setup:\s+(?:\(.*?\))(.*?)\s*Adversary')
    return boardRE.findall(text)

def parseAdversary( text ):
    #return a list of tuples (difficulty, adversary, level)
    adversaryRE = re.compile(r'(Beginner):\s*(.*?)\s+(\d+)\s*(Intermediate):\s*(.*?)\s+(\d+)\s*(Advanced):\s*(.*?)\s+(\d+)\s*(Expert):\s*(.*?)\s+(\d+)')
    advs = list(adversaryRE.findall(text)[0])
    return list( zip(advs[0::3],advs[1::3],advs[2::3]) )

def parseScenario( text ):
    #return the scenario to use in the challenge
    scenarioRE = re.compile(r'Scenario:.*?is:(.*?)\s*$')
    return scenarioRE.findall(text)

def parsePage( html ):
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # get the data from the HTML
    data = soup.find("div", attrs={"data-test-id": "post-content"})
    text = soup.getText()
    
    if( data == None ):
        print("     > ERROR: could not parse post content")
        #print("----------------------------------")
        #print(html)
        return None, None
    
    textRE = re.compile(r'(EXPANSION CONTENT:.*Results Formatting)')
    text = textRE.findall(text)
    if( text == None ):
        print("     > ERROR: could not parse post text")
        return None, None
    else:
        print("     + SUCCESS")

    title = data.contents[2].text.strip()
    post = data.contents[4].text.strip()

    raw_links = data.contents[4].find_all("a", string=re.compile(r'Week (\d+)'))
    links = {}
    for l in raw_links:
        print(l.text + " : " + l['href'] )
        
    return title, post

def parseChallenge( title, post ):
    #parse the challenge from the HTML
    challenge = Challenge(title)

    expansionRE = re.compile(r'(EXPANSION CONTENT:.*?)BASE GAME CONTENT')
    expansion = expansionRE.findall(post)[0]
    if( expansion != None ):
        challenge.expansionSpirits = parseSpirits(expansion)
        challenge.expansionBoardSetup = parseBoard(expansion)
        challenge.expansionAdversary = parseAdversary(expansion)
        challenge.expansionScenario = parseScenario(expansion)

    baseRE = re.compile(r'(BASE GAME CONTENT:.*?)Results Formatting')
    base = baseRE.findall(post)[0]
    if( base != None ):
        challenge.baseSpirits = parseSpirits(base)
        challenge.baseBoardSetup = parseBoard(base)
        challenge.baseAdversary = parseAdversary(base)
        challenge.baseScenario = parseScenario(base)

    return challenge


# iterate over the files in the data folder
for file in os.listdir("data"):
    # get the HTML from the file  
    if( file.startswith("challenge_Week") and file.endswith(".html") ):
        print("Parsing file: data/"+file)
        with open("data/"+file) as fp:
            html = fp.read()

        title, post = parsePage(html)
        if( title != None ):
            challenge = parseChallenge(title, post)
            print( "    + " + challenge.title )
        


# write the data to a CSV file
#with open("spirit_data.csv", "w") as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow(["Name", "Price", "Rating"])
#    for item in data:
#        name = item.find("h3", {"class": "product-name"}).text.strip()
#        price = item.find("span", {"class": "price"}).text.strip()
#        rating = item.find("span", {"class": "rating"}).text.strip()
#        writer.writerow([name, price, rating])




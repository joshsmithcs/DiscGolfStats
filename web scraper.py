import urllib
from bs4 import BeautifulSoup
import requests
import pandas as pd
import config

eventId = '77335'
roundNumber = 2
division = 'MPO'

def scrapePDGALive(eventId, roundNumber, division):
    url = f'https://www.pdga.com/apps/tournament/live/event?view=Scores&eventId={eventId}&round={roundNumber}&division={division}'
    
    def get_scrapeops_url(url):
        payload = {'api_key': config.API_KEY, 'url': url, 'bypass': 'cloudflare'}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urllib.parse.urlencode(payload)
        return proxy_url
    
    r = requests.get(get_scrapeops_url(url))
    f = open("pdgaLiveTest.txt", "w")
    f.write(r.text)
    f.close()

#scrapePDGALive(eventId,roundNumber,division)


f = open("pdgaLiveTest.txt", "r")
content = f.read()

soup = BeautifulSoup(content, "html.parser")
pdgaTable = soup.find("div", class_="pdga-table")

#Course Data
header = pdgaTable.find("div", class_="header-row")
cols = header.find_all("div", class_="header-col")

holes = []
lengths = []
pars = []
for i in range(5,len(cols)-2):
    holeHTML = cols[i]
    holes.append(int(holeHTML.find("div", class_="hole-header").get_text()))
    lengths.append(int(holeHTML.find("div", class_="hole-length").get_text()))
    pars.append(int(holeHTML.find("div", class_="hole-par").get_text()))
    
coursePar = sum(pars)
courseLength = sum(lengths)
numHoles = len(pars)

courseData =  {
    "hole number": holes,
    "hole length": lengths,
    "hole par": pars
}
courseDataDF = pd.DataFrame(courseData)
print(courseDataDF) 


#Player Data and Hole Data
body = pdgaTable.find("div", class_="table-body")
players = body.find_all("div", class_="table-row")

positions = []
names = []
tournamentScores = []
roundScores = []
roundTotals = []
roundRatings = []

holeScores = []

for player in players:
    position = player.find("div", class_="position-cell").find("span", class_="py-2").get_text()
    positions.append(position)
    firstName = player.find("span", class_="player-first-name").get_text()
    lastName = player.find("span", class_="player-last-name").get_text()
    fullName = f'{firstName} {lastName}'
    names.append(fullName)
    cells = player.find_all("div", class_="cell-wrapper")
    tournamentScore = cells[2].get_text()
    if tournamentScore == "E":
        tournamentScore = 0
    tournamentScores.append(int(tournamentScore))
    roundScore = int(cells[3].get_text())
    if roundScore == "E":
        roundScore = 0
    roundScores.append(int(roundScore))
    roundTotals.append(int(cells[-2].get_text()))
    roundRatings.append(int(cells[-1].get_text()))
    holes = []
    for i in range(5,len(cells)-2):
        holes.append(int(cells[i].get_text()))
    holeScores.append(holes)

playerData =  {
    "player name": names,
    "position": positions,
    "tournament scores": tournamentScores,
    "round score": roundScores,
    "round total": roundTotals,
    "round rating": roundRatings,
}
playerDataDF = pd.DataFrame(playerData)
print(playerDataDF) 

holeNumbers = []
for i in range(numHoles):
    holeNumbers.append(i+1)
    
holeDataDF = pd.DataFrame(holeScores, columns =holeNumbers)
print(holeDataDF.describe()) 

#Find Easiest and hardest holes
meanHoleDf = holeDataDF.mean()

print(meanHoleDf.to_list()) 
courseDataDF = courseDataDF.assign(mean=holeDataDF.mean().to_list())
courseDataDF = courseDataDF.assign(std=holeDataDF.std().to_list())
courseDataDF["average to par"] = courseDataDF["mean"] - courseDataDF["hole par"]-
print(courseDataDF)
holeAverageToPar = []
for i in range(numHoles):
    holeAverageToPar.append((courseDataDF["hole par"][i] - holeDataDF[i+1].mean(), i+1))


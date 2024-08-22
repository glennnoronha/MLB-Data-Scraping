from bs4 import BeautifulSoup
import requests

team_urls = {
    "ARI": "https://www.mlb.com/diamondbacks/roster/40-man",
    "ATL": "https://www.mlb.com/braves/roster/40-man",
    "BAL": "https://www.mlb.com/orioles/roster/40-man",
    "BOS": "https://www.mlb.com/redsox/roster/40-man",
    "CHC": "https://www.mlb.com/cubs/roster/40-man",
    "CHW": "https://www.mlb.com/whiteSox/roster/40-man",
    "CIN": "https://www.mlb.com/reds/roster/40-man",
    "CLE": "https://www.mlb.com/guardians/roster/40-man",
    "COL": "https://www.mlb.com/rockies/roster/40-man",
    "DET": "https://www.mlb.com/tigers/roster/40-man",
    "HOU": "https://www.mlb.com/astros/roster/40-man",
    "KC": "https://www.mlb.com/royals/roster/40-man",
    "LAA": "https://www.mlb.com/angels/roster/40-man",
    "LAD": "https://www.mlb.com/dodgers/roster/40-man",
    "MIA": "https://www.mlb.com/marlins/roster/40-man",
    "MIL": "https://www.mlb.com/brewers/roster/40-man",
    "MIN": "https://www.mlb.com/twins/roster/40-man",
    "NYM": "https://www.mlb.com/mets/roster/40-man",
    "NYY": "https://www.mlb.com/yankees/roster/40-man",
    "OAK": "https://www.mlb.com/athletics/roster/40-man",
    "PHI": "https://www.mlb.com/phillies/roster/40-man",
    "PIT": "https://www.mlb.com/pirates/roster/40-man",
    "SDP": "https://www.mlb.com/padres/roster/40-man",
    "SEA": "https://www.mlb.com/mariners/roster/40-man",
    "SFG": "https://www.mlb.com/giants/roster/40-man",
    "STL": "https://www.mlb.com/cardinals/roster/40-man",
    "TBR": "https://www.mlb.com/rays/roster/40-man",
    "TEX": "https://www.mlb.com/rangers/roster/40-man",
    "TOR": "https://www.mlb.com/bluejays/roster/40-man",
    "WSH": "https://www.mlb.com/nationals/roster/40-man"
}

for team, url in team_urls.items():
    result = requests.get(url)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")  
        #print(type(soup))
        forty_man = soup.find('div', 'players').find_all('table', 'roster__table')
        print(f"{team} 40-Man Roster:")
        counter = 1
        for roster in forty_man:
            players = roster.find('tbody').find_all('tr')
            for player in players:
                found_player = player.find('td', 'info').find('a')
                print(f"{counter}. {found_player.string}")
                counter += 1
        print("\n")
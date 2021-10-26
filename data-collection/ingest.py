import sys,requests,json,hashlib,pandas as pd,numpy as np
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import html
from requests.exceptions import HTTPError

def prefixRemove(row):
    return ' '.join(row.split(' ')[1:])

def createTeamID(row):
    m = hashlib.md5()
    m.update(row['Squad'].encode('utf-8'))
    return int(m.hexdigest(), 16)

def createPlayerID(row):
    m = hashlib.md5()
    m.update((row['Player'] + str(row['Born'])).encode('utf-8'))
    return int(m.hexdigest(), 16)

def getPreviousSeasons(table_func, years_back):
    dfs = [table_func(f'20{21-i}-20{22-i}') for i in range(years_back)]
    return pd.concat(dfs).reset_index(drop=True)

def getStandardStatsSquads(season='2021-2022'):
    # Retrieve team batting data from FB Ref
    url = f'https://fbref.com/en/comps/Big5/{season}/stats/squads/{season}-Big-5-European-Leagues-Stats'
    try:
        r = requests.get(url)
        # If the response was successful, no exception will be raised
        r.raise_for_status()
    except HTTPError as http_err:
        raise http_err

    # Retrieve Standard Stats Table from XML page and put into a DataFrame
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table', attrs=dict(id='stats_squads_standard_for'))

    teamdf = pd.read_html(str(table))[0]
    teamdf.columns = [' '.join(col) if col[0] == 'Per 90 Minutes' else col[1] for col in teamdf.columns.values]
    teamdf['League'] = teamdf.Comp.apply(prefixRemove)
    teamdf['Season'] = season
    teamdf['TeamID'] = teamdf.apply(createTeamID, axis=1)
    teamdf = teamdf.drop(columns=['Comp'])

    return teamdf

def getStandardStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/stats/players/{season}-Big-5-European-Leagues-Stats'
    try:
        r = requests.get(url)
        r.raise_for_status()
    except HTTPError as http_err:
        raise http_err

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table', attrs=dict(id='stats_standard'))

    playerdf = pd.read_html(str(table))[0]
    playerdf.columns = [' '.join(col) if col[0] == 'Per 90 Minutes' else col[1] for col in playerdf.columns.values]
    playerdf = playerdf[playerdf.Rk != 'Rk'].dropna(thresh=25)
    playerdf['Nation'] = playerdf.Nation.apply(prefixRemove)
    playerdf['League'] = playerdf.Comp.apply(prefixRemove)
    playerdf['Age'] = playerdf.Age.apply(lambda row: row.split('-')[0]) # Removing Age in days because it's only available for last couple seasons
    playerdf['Player'] = playerdf.Player.apply(lambda row: row.split('\\')[0])
    playerdf = playerdf.drop(columns=['Matches','Comp'])
    playerdf['Season'] = season
    playerdf['PlayerID'] = playerdf.apply(createPlayerID, axis=1)

    return playerdf
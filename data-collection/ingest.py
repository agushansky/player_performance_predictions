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
    return int(m.hexdigest(), 16) % 100000000000000000

def createPlayerID(row):
    m = hashlib.md5()
    m.update((row['Player'] + str(row['Born'])).encode('utf-8'))
    return int(m.hexdigest(), 16) % 100000000000

def getDF(url, table_id):
    try:
        r = requests.get(url)
        # If the response was successful, no exception will be raised
        r.raise_for_status()
    except HTTPError as http_err:
        raise http_err

    # Retrieve Standard Stats Table from XML page and put into a DataFrame
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table', attrs=dict(id=table_id))

    return pd.read_html(str(table))[0]

def teamPreprocess(teamdf, season):
    teamdf['League'] = teamdf.Comp.apply(prefixRemove)
    teamdf['Season'] = season
    teamdf['TeamID'] = teamdf.apply(createTeamID, axis=1)
    teamdf = teamdf.drop(columns=['Comp'])

    return teamdf.fillna(0)

def playerPreprocess(playerdf, season):
    playerdf = playerdf[playerdf.Rk != 'Rk'].dropna(thresh=25)
    playerdf['Nation'] = playerdf.Nation.apply(prefixRemove)
    playerdf['League'] = playerdf.Comp.apply(prefixRemove)
    playerdf['Age'] = playerdf.Age.apply(lambda row: row.split('-')[0]) # Removing Age in days because it's only available for last couple seasons
    playerdf['Player'] = playerdf.Player.apply(lambda row: row.split('\\')[0])
    playerdf = playerdf.drop(columns=['Matches','Comp'])
    playerdf['Season'] = season
    playerdf['PlayerID'] = playerdf.apply(createPlayerID, axis=1)

    return playerdf.fillna(0)

def getPreviousSeasons(table_func, years_back):
    dfs = [table_func(f'20{21-i}-20{22-i}') for i in range(years_back)]
    return pd.concat(dfs).reset_index(drop=True)

def getStandardStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/stats/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_standard_for')
    teamdf.columns = [' '.join(col) if col[0] == 'Per 90 Minutes' else col[1] for col in teamdf.columns.values]

    return teamPreprocess(teamdf, season)

def getStandardStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/stats/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_standard')
    playerdf.columns = [' '.join(col) if col[0] == 'Per 90 Minutes' else col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getGoalkeepingStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/keepers/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_keeper_for')
    teamdf.columns = [col[1] for col in teamdf.columns.values]

    return teamPreprocess(teamdf, season)

def getGoalkeepingStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/keepers/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_keeper')
    playerdf.columns = [col[1] for col in playerdf.columns.values]

    return playerPreprocess(playerdf, season)

def getAdvGoalkeepingStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/keepersadv/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_keeper_adv_for')
    teamdf.columns = [' '.join(col) if 'Unnamed' not in col[0] else col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getAdvGoalkeepingStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/keepersadv/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_keeper_adv')
    playerdf.columns = [' '.join(col) if 'Unnamed' not in col[0] else col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getShootingStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/shooting/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_shooting_for')
    teamdf.columns = [col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getShootingStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/shooting/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_shooting')
    playerdf.columns = [col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getPassingStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/passing/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_passing_for')
    teamdf.columns = [' '.join(col) if 'Unnamed' not in col[0] else col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getPassingStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/passing/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_passing')
    playerdf.columns = [' '.join(col) if 'Unnamed' not in col[0] else col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getPassTypesStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/passing_types/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_passing_types_for')
    teamdf.columns = [': '.join(col) if 'Unnamed' not in col[0] else col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getPassTypesStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/passing_types/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_passing_types')
    playerdf.columns = [': '.join(col) if 'Unnamed' not in col[0] else col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getGoalShotCreationStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/gca/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_gca_for')
    teamdf.columns = [col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getGoalShotCreationStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/gca/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_gca')
    playerdf.columns = [col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getDefenseStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/defense/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_defense_for')
    teamdf.columns = [': '.join(col) if 'Unnamed' not in col[0] else col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getDefenseStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/defense/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_defense')
    playerdf.columns = [': '.join(col) if 'Unnamed' not in col[0] else col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getPossessionStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/possession/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_possession_for')
    teamdf.columns = [col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getPossessionStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/possession/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_possession')
    playerdf.columns = [col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getPlayingTimeStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/playingtime/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_playing_time_for')
    teamdf.columns = [col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getPlayingTimeStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/playingtime/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_playing_time')
    playerdf.columns = [col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)

def getMiscStatsSquads(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/misc/squads/{season}-Big-5-European-Leagues-Stats'
    teamdf = getDF(url, 'stats_squads_misc_for')
    teamdf.columns = [col[1] for col in teamdf.columns.values]
    
    return teamPreprocess(teamdf, season)

def getMiscStatsPlayers(season='2021-2022'):
    url = f'https://fbref.com/en/comps/Big5/{season}/misc/players/{season}-Big-5-European-Leagues-Stats'
    playerdf = getDF(url, 'stats_misc')
    playerdf.columns = [col[1] for col in playerdf.columns.values]
    
    return playerPreprocess(playerdf, season)
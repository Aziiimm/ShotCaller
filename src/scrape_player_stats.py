import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

team_name_mapping = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BRK": "Brooklyn Nets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHO": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards"
}

def remove_accents(input_str):
    """
    This function removes accents from a given string using Unicode normalization.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def scrape_player_stats():
    url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'id': 'per_game_stats'})

    headers = [th.getText() for th in table.find_all('tr')[0].find_all('th')][1:]  # skip the 'rank' column

    rows = table.find_all('tr')[1:]
    player_stats = [[td.getText() for td in row.find_all('td')] for row in rows if row.find('td')]

    df = pd.DataFrame(player_stats, columns=headers)

    # disregard 'League Average' row
    df = df[df['Player'] != 'League Average']

    df['Player'] = df['Player'].apply(remove_accents)

    df['Team'] = df['Team'].map(team_name_mapping)

    relevant_columns = ['Player', 'Team', 'Pos', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    df = df[relevant_columns]

    numeric_columns = ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    df.to_csv('nba_player_stats_2024.csv', index=False, encoding='utf-8')
    print("Player stats saved to nba_player_stats_2024.csv")

    return df

if __name__ == "__main__":
    scrape_player_stats()

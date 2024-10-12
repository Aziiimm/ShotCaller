import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

def remove_accents(input_str):
    """
    This function removes accents from a given string using Unicode normalization.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def scrape_player_stats():
    url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
    response = requests.get(url)

    # set encoding to UTF-8
    response.encoding = 'utf-8'

    # check for sucessful request 
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return None

    # parse html content
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the table
    table = soup.find('table', {'id': 'per_game_stats'})

    # extract headers
    headers = [th.getText() for th in table.find_all('tr')[0].find_all('th')][1:]  # skip the 'rank' column

    # extract rows
    rows = table.find_all('tr')[1:]
    player_stats = [[td.getText() for td in row.find_all('td')] for row in rows if row.find('td')]

    # convert to dataframe
    df = pd.DataFrame(player_stats, columns=headers)

    # disregard 'League Average' row
    df = df[df['Player'] != 'League Average']

    # print("Original player names:")
    # print(df['Player'].head(10))  # Print the first 10 players

    # remove accent marks
    df['Player'] = df['Player'].apply(remove_accents)

    # print("Updated player names:")
    # print(df['Player'].head(10))  # Print the first 10 players

    relevant_columns = ['Player', 'Team', 'Pos', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    df = df[relevant_columns]

    numeric_columns = ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    df.to_csv('nba_player_stats_2024.csv', index=False, encoding='utf-8')
    print("Player stats saved to nba_player_stats_2024.csv")

    return df

if __name__ == "__main__":
    scrape_player_stats()

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_player_stats():
    url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
    response = requests.get(url)

    # check if request is successful
    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return None

    # parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the table
    table = soup.find('table', {'id': 'per_game_stats'})

    # extract headers
    headers = [th.getText() for th in table.find_all('tr')[0].find_all('th')][1:]  # skip the rank column

    # extract rows
    rows = table.find_all('tr')[1:]
    player_stats = [[td.getText() for td in row.find_all('td')] for row in rows if row.find('td')]

    # convert to dataframe
    df = pd.DataFrame(player_stats, columns=headers)

    # save to csv
    df.to_csv('nba_player_stats_2024.csv', index=False)
    print("Player stats saved to nba_player_stats_2024.csv")


if __name__ == "__main__":
    scrape_player_stats()
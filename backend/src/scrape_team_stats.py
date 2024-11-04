import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_team_advanced_stats():
    url = 'https://www.basketball-reference.com/leagues/NBA_2024.html'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching page: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the advanced stats table
    table = soup.find('table', {'id': 'advanced-team'})

    # Extract headers for the required columns
    headers = ['Team', 'W', 'L', 'MOV', 'ORtg', 'DRtg', 'NRtg', 'TS%']

    # Extract rows
    rows = table.find_all('tr')[1:]  # Skip the header row
    team_stats = []

    for row in rows:
        data = row.find_all('td')
        if data:  # Ensure the row contains data
            team_data = [
                data[0].getText().replace('*', '').strip(),  # Team name
                data[2].getText(),  # Wins
                data[3].getText(),  # Losses
                data[6].getText(),  # Margin of Victory (MOV)
                data[9].getText(),  # Offensive Rating (ORtg)
                data[10].getText(),  # Defensive Rating (DRtg)
                data[11].getText(),  # Net Rating (NRtg)
                data[15].getText()   # True Shooting Percentage (TS%)
            ]
            team_stats.append(team_data)

    # Create DataFrame
    df = pd.DataFrame(team_stats, columns=headers)
    df = df[df['Team'] != 'League Average']

    # Clean the DataFrame (convert numeric columns to appropriate types)
    numeric_columns = ['W', 'L', 'MOV', 'ORtg', 'DRtg', 'NRtg', 'TS%']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Save to CSV
    df.to_csv('nba_team_advanced_stats_2024.csv', index=False)

    print("Team advanced stats saved to nba_team_advanced_stats_2024.csv")
    return df

if __name__ == "__main__":
    df = scrape_team_advanced_stats()
    if df is not None:
        print(df.head())

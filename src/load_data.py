import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection string
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Create database engine
engine = create_engine(DATABASE_URL)

# Load data from PostgreSQL into pandas DataFrame
player_df = pd.read_sql('SELECT * FROM player_stats', engine)
team_df = pd.read_sql('SELECT * FROM team_stats', engine)

player_df['rebounds_per_game'] = player_df['total_rebounds'] / player_df['games_played']

# Calculate team-level averages for points, assists, and rebounds
team_averages = player_df.groupby('team').agg({
    'points_per_game': 'mean',
    'assists_per_game': 'mean',
    'rebounds_per_game': 'mean'
}).reset_index()

# Merge team averages with the team dataframe
team_df = pd.merge(team_df, team_averages, on='team', how='inner')

# Ensure 'win_percentage' column exists in team_df
team_df['win_percentage'] = team_df['wins'] / (team_df['wins'] + team_df['losses'])

# Create matchups between two teams (hypothetical or historical)
matchups = []

for i in range(len(team_df) - 1):
    for j in range(i + 1, len(team_df)):
        team_A = team_df.iloc[i]
        team_B = team_df.iloc[j]
        
        # Create matchup features: Team A vs Team B
        matchup = {
            'team_A_win_percentage': team_A['win_percentage'],
            'team_A_points_per_game': team_A['points_per_game'],
            'team_A_assists_per_game': team_A['assists_per_game'],
            'team_A_rebounds_per_game': team_A['rebounds_per_game'],
            'team_A_top_player_points': player_df[player_df['team'] == team_A['team']]['points_per_game'].max(),

            'team_B_win_percentage': team_B['win_percentage'],
            'team_B_points_per_game': team_B['points_per_game'],
            'team_B_assists_per_game': team_B['assists_per_game'],
            'team_B_rebounds_per_game': team_B['rebounds_per_game'],
            'team_B_top_player_points': player_df[player_df['team'] == team_B['team']]['points_per_game'].max(),
            
            # Target: 1 if Team A won, 0 if Team B won (for now, random or historical data)
            'match_outcome': 1 if team_A['wins'] > team_B['wins'] else 0
        }
        matchups.append(matchup)

# Convert matchups into DataFrame
matchup_df = pd.DataFrame(matchups)

# Save to CSV
matchup_df.to_csv('team_matchups.csv', index=False)

if __name__ == "__main__":
    print(matchup_df.head())


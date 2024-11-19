import pandas as pd
import numpy as np

# Load player stats
player_df = pd.read_csv('../data/nba_player_stats_2024.csv')

# Calculate fantasy points
player_df['fantasy_points'] = (
    player_df['PTS'] * 1 + 
    player_df['AST'] * 1.5 + 
    player_df['TRB'] * 1.2 + 
    player_df['STL'] * 3 + 
    player_df['BLK'] * 3
)

# Generate matchups
matchups = []

# Simulate 10,000 matchups
num_matchups = 10000
for _ in range(num_matchups):
    team_A_players = player_df.sample(10)  # Randomly select 10 players for Team A
    team_B_players = player_df.sample(10)  # Randomly select 10 players for Team B

    team_A_score = team_A_players['fantasy_points'].sum()
    team_B_score = team_B_players['fantasy_points'].sum()

    # Stat differentials
    matchup = {
        'team_A_score': team_A_score,
        'team_B_score': team_B_score,
        'PTS_diff': team_A_players['PTS'].sum() - team_B_players['PTS'].sum(),
        'AST_diff': team_A_players['AST'].sum() - team_B_players['AST'].sum(),
        'TRB_diff': team_A_players['TRB'].sum() - team_B_players['TRB'].sum(),
        'STL_diff': team_A_players['STL'].sum() - team_B_players['STL'].sum(),
        'BLK_diff': team_A_players['BLK'].sum() - team_B_players['BLK'].sum(),
        'match_outcome': 1 if team_A_score > team_B_score else 0
    }
    matchups.append(matchup)

# Convert to DataFrame
matchup_df = pd.DataFrame(matchups)

# Save the dataset
matchup_df.to_csv('../data/fantasy_matchups.csv', index=False)

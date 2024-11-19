from flask import Blueprint, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

predict_app = Blueprint('predict-nba', __name__)
CORS(predict_app)

model = joblib.load('./models/random_forest_matchup_model.pkl')
matchup_df = pd.read_csv('./data/team_matchups.csv')

@predict_app.route('/predict-nba', methods=['POST'])
def predict_nba():
    data = request.json
    team_A = data['team_A']
    team_B = data['team_B']

    team_A_data = matchup_df[matchup_df['team_A'] == team_A]
    team_B_data = matchup_df[matchup_df['team_B'] == team_B]

    if team_A_data.empty or team_B_data.empty:
        return jsonify({'error': 'One or both teams not found'}), 400

    team_A_data = team_A_data.iloc[0]
    team_B_data = team_B_data.iloc[0]

    input_data = pd.DataFrame({
        'team_A_win_percentage': [team_A_data['team_A_win_percentage']],
        'team_A_points_per_game': [team_A_data['team_A_points_per_game']],
        'team_A_assists_per_game': [team_A_data['team_A_assists_per_game']],
        'team_A_rebounds_per_game': [team_A_data['team_A_rebounds_per_game']],
        'team_A_top_player_points': [team_A_data['team_A_top_player_points']],
        'team_B_win_percentage': [team_B_data['team_B_win_percentage']],
        'team_B_points_per_game': [team_B_data['team_B_points_per_game']],
        'team_B_assists_per_game': [team_B_data['team_B_assists_per_game']],
        'team_B_rebounds_per_game': [team_B_data['team_B_rebounds_per_game']],
        'team_B_top_player_points': [team_B_data['team_B_top_player_points']]
    })

    # Make prediction using the model
    prediction = model.predict(input_data)

    # Return prediction as a response
    result = f"{team_A} Wins" if prediction[0] == 1 else f"{team_B} Wins"
    return jsonify({'prediction': result})


fantasy_model = joblib.load('./models/random_forest_fantasy_model.pkl')
scaler = joblib.load('./models/fantasy_scaler.pkl')
fantasy_player_stats = pd.read_csv('./data/nba_player_stats_2024.csv')

@predict_app.route('/predict-fantasy', methods=['POST'])
def predict_fantasy():
    data = request.json
    team_A_players = data['team_A_players']
    team_B_players = data['team_B_players']

    # Fetch player stats
    team_A_stats = fantasy_player_stats[fantasy_player_stats['Player'].isin(team_A_players)].copy()
    team_B_stats = fantasy_player_stats[fantasy_player_stats['Player'].isin(team_B_players)].copy()

    if team_A_stats.empty or team_B_stats.empty:
        return jsonify({'error': 'Invalid player selections'}), 400

    team_A_stats['fantasy_points'] = (
        team_A_stats['PTS'] * 1 +
        team_A_stats['AST'] * 1.5 +
        team_A_stats['TRB'] * 1.2 +
        team_A_stats['STL'] * 3 +
        team_A_stats['BLK'] * 3
    )

    team_B_stats['fantasy_points'] = (
        team_B_stats['PTS'] * 1 +
        team_B_stats['AST'] * 1.5 +
        team_B_stats['TRB'] * 1.2 +
        team_B_stats['STL'] * 3 +
        team_B_stats['BLK'] * 3
    )

    # Calculate total scores and stat differentials
    team_A_score = team_A_stats['fantasy_points'].sum()
    team_B_score = team_B_stats['fantasy_points'].sum()

    stat_differentials = {
        "PTS_diff": team_A_stats['PTS'].sum() - team_B_stats['PTS'].sum(),
        "AST_diff": team_A_stats['AST'].sum() - team_B_stats['AST'].sum(),
        "TRB_diff": team_A_stats['TRB'].sum() - team_B_stats['TRB'].sum(),
        "STL_diff": team_A_stats['STL'].sum() - team_B_stats['STL'].sum(),
        "BLK_diff": team_A_stats['BLK'].sum() - team_B_stats['BLK'].sum(),
    }

    # Normalize input
    input_data = pd.DataFrame([{
        'team_A_score': team_A_score,
        'team_B_score': team_B_score,
        **stat_differentials
    }])
    input_data_normalized = scaler.transform(input_data)

    # Predict outcome
    prediction = fantasy_model.predict(input_data_normalized)
    result = "Team A Wins" if prediction[0] == 1 else "Team B Wins"

    # Return prediction and details
    return jsonify({
        'prediction': result,
        'team_A_score': team_A_score,
        'team_B_score': team_B_score,
        'stat_differentials': stat_differentials
    })
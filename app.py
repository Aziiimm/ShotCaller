from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

model = joblib.load('./models/random_forest_matchup_model.pkl')

matchup_df = pd.read_csv('./data/team_matchups.csv')
print(matchup_df.columns)


# route to handle prediction request
@app.route('/predict', methods=['POST'])
def predict():
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

if __name__ == "__main__":
    app.run(debug=True)
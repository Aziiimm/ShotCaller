import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the matchup data
matchup_df = pd.read_csv('team_matchups.csv')

# Select features for Team A and Team B stats
X = matchup_df[['team_A_win_percentage', 'team_A_points_per_game', 'team_A_assists_per_game', 
                'team_A_rebounds_per_game', 'team_A_top_player_points', 
                'team_B_win_percentage', 'team_B_points_per_game', 'team_B_assists_per_game', 
                'team_B_rebounds_per_game', 'team_B_top_player_points']]

# Target: Which team won (Team A = 1, Team B = 0)
y = matchup_df['match_outcome']

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize RandomForestClassifier
rf_model = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=5, random_state=42, class_weight={0: 2, 1: 1})

# Train the model
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Display feature importance
importances = rf_model.feature_importances_
feature_names = X.columns
feature_names_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
print(feature_names_df.sort_values(by='Importance', ascending=False))

# Save the trained model for future use
joblib.dump(rf_model, 'random_forest_matchup_model.pkl')

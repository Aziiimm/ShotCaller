from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib

# Load data
fantasy_matchup_df = pd.read_csv('../data/fantasy_matchups.csv')

# Select features and target
X = fantasy_matchup_df[['team_A_score', 'team_B_score', 'PTS_diff', 'AST_diff', 'TRB_diff', 'STL_diff', 'BLK_diff']]
y = fantasy_matchup_df['match_outcome']

# Normalize features
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

# Train the Random Forest model
fantasy_model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight={0: 1, 1: 1})
fantasy_model.fit(X_train, y_train)

# Test the model
y_pred = fantasy_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model and scaler
joblib.dump(fantasy_model, '../models/random_forest_fantasy_model.pkl')
joblib.dump(scaler, '../models/fantasy_scaler.pkl')

# Cross-validation scores
scores = cross_val_score(fantasy_model, X_normalized, y, cv=5)
print(f"Cross-Validation Scores: {scores}")
print(f"Mean Accuracy: {scores.mean() * 100:.2f}%")

importances = fantasy_model.feature_importances_
feature_names = X.columns
for feature, importance in zip(feature_names, importances):
    print(f"{feature}: {importance:.4f}")
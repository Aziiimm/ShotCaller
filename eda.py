import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from load_data import player_df, team_df  # Import the cleaned player stats

merged_df = pd.merge(player_df, team_df, on='team', how='inner')
print(merged_df.head(10))

# Distribution of Points Per Game
sns.histplot(merged_df['points_per_game'], kde=True)
plt.title('Distribution of Points Per Game')
plt.xlabel('Points Per Game')
plt.ylabel('Frequency')
plt.show()

numeric_cols = merged_df.select_dtypes(include=['float64', 'int64'])

# Correlation Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix of Player and Team Stats')
plt.show()

# Boxplot of Points Per Game by Position
sns.boxplot(x='position', y='points_per_game', data=merged_df)
plt.title('Points Per Game by Position')
plt.xlabel('Position')
plt.ylabel('Points Per Game')
plt.show()

# Scatter Plot with Linear Regression
sns.lmplot(x='field_goals_made', y='points_per_game', data=merged_df, aspect=1.5, scatter_kws={'alpha':0.5})
plt.title('Field Goals Made vs Points Per Game')
plt.show()

# Pairplot for Multiple Features
sns.pairplot(merged_df[['field_goals_made', 'three_pointers_made', 'free_throws_made', 'points_per_game']])
plt.show()

# Group by Team and Calculate Averages
team_stats = merged_df.groupby('team').mean(numeric_only=True)
print(team_stats.head())

# Bar Plot of Average Points Per Game by Team
team_stats_sorted = team_stats.sort_values('points_per_game', ascending=False)
team_stats_sorted['points_per_game'].plot(kind='bar', figsize=(12, 6))
plt.title('Average Points Per Game by Team')
plt.xlabel('Team')
plt.ylabel('Points Per Game')
plt.show()

# Bar Pot of Team Wins vs Average Player PPG
sns.barplot(x='wins', y='points_per_game', data=merged_df)
plt.title('Team Wins vs Average Player Points Per Game')
plt.xlabel('Team Wins')
plt.ylabel('Average Player Points Per Game')
plt.show()

# Scatter Plot of Team Assists vs Player Points Per Game
sns.lmplot(x='assists_per_game', y='points_per_game', data=merged_df, aspect=1.5, scatter_kws={'alpha':0.5})
plt.title('Team Assists Per Game vs Player Points Per Game')
plt.show()

# Box Plot of Wins vs Player PPG by Position
sns.boxplot(x='position', y='points_per_game', hue='wins', data=merged_df)
plt.title('Team Wins vs. Player Points Per Game by Position')
plt.xlabel('Position')
plt.ylabel('Points Per Game')
plt.show()

# Scatter Plot of Defensive Stats vs PPG
sns.lmplot(x='blocks_per_game', y='points_per_game', data=merged_df, aspect=1.5, scatter_kws={'alpha':0.5})
plt.title('Team Blocks Per Game vs Player Points Per Game')
plt.show()

# Violin Plot of PPG by Team
sns.violinplot(x='team', y='points_per_game', data=merged_df, inner="quartile")
plt.xticks(rotation=90)
plt.title('Distribution of Player Points Per Game Across Teams')
plt.show()

# Barplot of Player Contribution to Team Wins
sns.barplot(x='team', y='wins', hue='player', data=merged_df)
plt.xticks(rotation=90)
plt.title('Contribution of Players to Team Wins')
plt.show()

print(team_stats[['points_per_game', 'assists_per_game']].describe())

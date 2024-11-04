import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.load_data import merged_df  # Import the cleaned player stats

print(merged_df.head(10))

# distribution of player ppg, shows how player performance varies
sns.histplot(merged_df['points_per_game'], kde=True)
plt.title('Distribution of Points Per Game')
plt.xlabel('Points Per Game')
plt.ylabel('Frequency')
plt.show()



numeric_cols = merged_df.select_dtypes(include=['float64', 'int64'])
# correlation heatmap to detect relationships between variables
plt.figure(figsize=(12, 8))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix of Player and Team Stats')
plt.show()

# show how position affects ppg, could show how role affects win %
sns.boxplot(x='position', y='points_per_game', data=merged_df)
plt.title('Points Per Game by Position')
plt.xlabel('Position')
plt.ylabel('Points Per Game')
plt.show()

# show relationship between field goals made and ppg, for insight on individual player performance
sns.lmplot(x='field_goals_made', y='points_per_game', data=merged_df, aspect=1.5, scatter_kws={'alpha':0.5})
plt.title('Field Goals Made vs Points Per Game')
plt.show()

# useful for spotting relationships between performance metrics
sns.pairplot(merged_df[['field_goals_made', 'three_pointers_made', 'free_throws_made', 'points_per_game']])
plt.show()

team_stats = merged_df.groupby('team').mean(numeric_only=True)
print(team_stats.head())

# insight on overall team performance
team_stats_sorted = team_stats.sort_values('points_per_game', ascending=False)
team_stats_sorted['points_per_game'].plot(kind='bar', figsize=(12, 6))
plt.title('Average Points Per Game by Team')
plt.xlabel('Team')
plt.ylabel('Points Per Game')
plt.show()

# shows impact of individual player performance on team success
sns.barplot(x='wins', y='points_per_game', data=merged_df)
plt.title('Team Wins vs Average Player Points Per Game')
plt.xlabel('Team Wins')
plt.ylabel('Average Player Points Per Game')
plt.show()

# show how assist affects player performance
sns.lmplot(x='assists_per_game', y='points_per_game', data=merged_df, aspect=1.5, scatter_kws={'alpha':0.5})
plt.title('Team Assists Per Game vs Player Points Per Game')
plt.show()

# show which position may have the biggest impact on team success
sns.boxplot(x='position', y='points_per_game', hue='wins', data=merged_df)
plt.title('Team Wins vs. Player Points Per Game by Position')
plt.xlabel('Position')
plt.ylabel('Points Per Game')
plt.show()

# show how defense may affect team ppg
sns.lmplot(x='blocks_per_game', y='points_per_game', data=merged_df, aspect=1.5, scatter_kws={'alpha':0.5})
plt.title('Team Blocks Per Game vs Player Points Per Game')
plt.show()

# show offensive capabilities of diff teams
sns.violinplot(x='team', y='points_per_game', data=merged_df, inner="quartile")
plt.xticks(rotation=90)
plt.title('Distribution of Player Points Per Game Across Teams')
plt.show()

# show how indivdiual players contribute to team wins
sns.barplot(x='team', y='wins', hue='player', data=merged_df)
plt.xticks(rotation=90)
plt.title('Contribution of Players to Team Wins')
plt.show()

# show distribution of win percentage
sns.histplot(merged_df['win_percentage'], kde=True)
plt.title('Distribution of Win Percentage')
plt.xlabel('Win Percentage')
plt.ylabel('Frequency')
plt.show()

# show how players impact team success
sns.lmplot(x='player_impact', y='points_per_game', data=merged_df, aspect=1.5)
plt.title('Player Impact vs Points Per Game')
plt.show()

print(team_stats[['points_per_game', 'assists_per_game']].describe())

import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def load_team_advanced_stats_to_postgres():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

    cur = conn.cursor()

    team_stats_df = pd.read_csv('nba_team_advanced_stats_2024.csv')

    print(team_stats_df.head())  # Check the first few rows of the DataFrame
    print(team_stats_df.dtypes)   # Check the data types of each column

    team_stats_df.fillna(0, inplace=True)

    team_stats_df['W'] = pd.to_numeric(team_stats_df['W'], errors='coerce').fillna(0).astype(int)
    team_stats_df['L'] = pd.to_numeric(team_stats_df['L'], errors='coerce').fillna(0).astype(int)

    for i, row in team_stats_df.iterrows():
        cur.execute("""
            INSERT INTO team_stats (team, wins, losses, margin_of_victory, offensive_rating, defensive_rating, net_rating, true_shooting_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (team) DO NOTHING  -- Avoid duplicate entries
        """, tuple(row))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_team_advanced_stats_to_postgres()
from dotenv import load_dotenv
import os
import psycopg2
from scrape_nba import scrape_player_stats

load_dotenv()

def save_to_postgres(df):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

    conn.set_client_encoding('UTF-8')
    cur = conn.cursor()

    for i, row in df.iterrows():
        print(f"Inserting row: {row}")
        print(f"Row type: {type(row)}")  

        # extracting only the values from the row
        row_values = tuple(row.values)
        print(f"Row values: {row_values}") 

        cur.execute("""
            INSERT INTO player_stats (player, team, position, games_played, minutes_per_game, 
                                      field_goals_made, field_goals_attempted, field_goal_percentage, 
                                      three_pointers_made, three_pointers_attempted, three_point_percentage, 
                                      free_throws_made, free_throws_attempted, free_throw_percentage, 
                                      offensive_rebounds, defensive_rebounds, total_rebounds, 
                                      assists_per_game, steals_per_game, blocks_per_game, 
                                      turnovers_per_game, personal_fouls_per_game, points_per_game)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, row_values)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    df = scrape_player_stats()
    if df is not None:
        save_to_postgres(df)
    else:
        print("Failed to scrape player stats")

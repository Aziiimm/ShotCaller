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

# Show all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

if __name__ == "__main__":


    # print(player_df.head())
    # print('__________________________________________________')
    # print(player_df.isnull().sum())
    # print('__________________________________________________')
    # print(player_df.describe())
    # print('__________________________________________________')
 
 
    print(team_df)
    print('__________________________________________________')
    print(team_df.isnull().sum())
    print('__________________________________________________')
    print(team_df.describe())

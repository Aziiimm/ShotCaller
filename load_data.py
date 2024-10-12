import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# database connection string
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# create database engine
engine = create_engine(DATABASE_URL)

# load data from postgresql into panadas dataframe
df = pd.read_sql('SELECT * FROM player_stats', engine)

# show all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# fill in zero for missing values
df['field_goal_percentage'].fillna(0, inplace=True)
df['three_point_percentage'].fillna(0, inplace=True)
df['free_throw_percentage'].fillna(0, inplace=True)

print(df.head())
print('__________________________________________________')
print(df.isnull().sum())
print('__________________________________________________')
print(df.describe())
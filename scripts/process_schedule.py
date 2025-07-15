import os
import pandas as pd
from datetime import timedelta

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RAW_CSV = os.path.join(DATA_DIR, 'weekly_games.csv')
PROCESSED_CSV = os.path.join(DATA_DIR, 'processed_weekly_games.csv')

# List of official NBA team abbreviations
NBA_TEAMS = [
    'ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
    'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
    'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]


def add_week_column(df):
    """
    Adds a 'WEEK' column to the DataFrame based on GAME_DATE (ISO week number).
    """
    df['WEEK'] = df['GAME_DATE'].dt.isocalendar().week
    df['YEAR'] = df['GAME_DATE'].dt.year
    df['DAY_NAME'] = df['GAME_DATE'].dt.day_name()
    return df


def mark_back_to_backs(df):
    """
    Adds a 'BACK_TO_BACK' column: True if a team plays on consecutive days.
    """
    df = df.sort_values(['TEAM_ABBREVIATION', 'GAME_DATE'])
    df['PREV_GAME_DATE'] = df.groupby('TEAM_ABBREVIATION')['GAME_DATE'].shift(1)
    df['PREV_DAY_NAME'] = df.groupby('TEAM_ABBREVIATION')['DAY_NAME'].shift(1)
    df['BACK_TO_BACK'] = (df['GAME_DATE'] - df['PREV_GAME_DATE']) == timedelta(days=1)
    df['BACK_TO_BACK'] = df['BACK_TO_BACK'].fillna(False)
    return df


def get_b2b_days(df):
    # For each team/week, find all (prev_day, curr_day) pairs where BACK_TO_BACK is True
    b2b_days = (
        df[df['BACK_TO_BACK']]
        .groupby(['TEAM_ABBREVIATION', 'YEAR', 'WEEK'])
        .apply(lambda g: '/'.join([f"{row.PREV_DAY_NAME[:3]}/{row.DAY_NAME[:3]}" for _, row in g.iterrows()]))
        .reset_index(name='b2b_days')
    )
    return b2b_days


def count_games_per_week(df, b2b_days):
    """
    Returns a DataFrame with games per team per week, and back-to-back info for each game.
    """
    # Group by team, year, week, and aggregate
    weekly = df.groupby(['TEAM_ABBREVIATION', 'YEAR', 'WEEK']).agg(
        games_played=('GAME_ID', 'count'),
        back_to_backs=('BACK_TO_BACK', 'sum')
    ).reset_index()
    weekly = weekly.merge(b2b_days, on=['TEAM_ABBREVIATION', 'YEAR', 'WEEK'], how='left')
    weekly['b2b_days'] = weekly['b2b_days'].fillna('')
    return weekly


def main():
    if not os.path.exists(RAW_CSV):
        print(f"Input file not found: {RAW_CSV}")
        return
    df = pd.read_csv(RAW_CSV, parse_dates=['GAME_DATE'])
    print(f"Loaded {len(df)} games.")
    # Filter for only NBA teams
    df = df[df['TEAM_ABBREVIATION'].isin(NBA_TEAMS)]
    print(f"Filtered to {df['TEAM_ABBREVIATION'].nunique()} NBA teams and {len(df)} games.")
    df = add_week_column(df)
    df = mark_back_to_backs(df)
    b2b_days = get_b2b_days(df)
    weekly = count_games_per_week(df, b2b_days)
    weekly.to_csv(PROCESSED_CSV, index=False)
    print(f"Processed data saved to {PROCESSED_CSV}")
    print(weekly.head())

if __name__ == "__main__":
    main() 
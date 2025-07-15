import os
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import SeasonAll
from datetime import datetime

# Constants
SEASON = '2023-24'  # NBA season format for nba_api
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CSV_PATH = os.path.join(DATA_DIR, 'weekly_games.csv')


def fetch_nba_schedule(season=SEASON):
    """
    Fetches NBA regular season schedule for the given season using nba_api.
    Returns a DataFrame with game date, teams, and game ID.
    """
    print(f"Fetching NBA schedule for {season}...")
    try:
        gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable='Regular Season')
        games = gamefinder.get_data_frames()[0]
        print(f"Fetched {len(games)} rows from nba_api.")
        # Only keep necessary columns
        games = games[['GAME_ID', 'GAME_DATE', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'MATCHUP']]
        # Convert GAME_DATE to datetime
        games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])
        print("Sample data:")
        print(games.head())
        return games
    except Exception as e:
        print(f"Error fetching NBA schedule: {e}")
        return pd.DataFrame()


def save_schedule_to_csv(df, path=CSV_PATH):
    """
    Saves the DataFrame to a CSV file at the given path.
    """
    try:
        if df.empty:
            print("No data to save.")
            return
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Saved schedule to {path}")
    except Exception as e:
        print(f"Error saving CSV: {e}")


def main():
    schedule_df = fetch_nba_schedule()
    save_schedule_to_csv(schedule_df)

if __name__ == "__main__":
    main() 
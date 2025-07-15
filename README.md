# NBA Fantasy Dashboard

A **Streamlit dashboard** to visualize how many games each NBA team plays per week during the 2023-24 regular season, including highlights for back-to-back games. Data is fetched from the NBA API and processed with pandas.

## Features
- ✅ Filter by team and week
- ✅ Table of games per week for each team
- ✅ Visual highlight for weeks with back-to-back games

## 📁 Folder Structure
nba-fantasy-dashboard/
├── data/ # CSV data files
├── scripts/ # Data fetching and processing scripts
│ ├── fetch_schedule.py # Fetches NBA schedule from nba_api
│ └── process_schedule.py # Processes schedule for weekly and back-to-back info
├── app.py # Streamlit dashboard
├── requirements.txt # Python dependencies
└── README.md # This file


## 🚀 Setup

1. **Clone the repository and navigate to the project folder:**
   ```bash
   git clone <your-repo-url>
   cd nba-fantasy-dashboard
Install dependencies:



pip install -r requirements.txt
Fetch and process NBA schedule data:


python scripts/fetch_schedule.py
python scripts/process_schedule.py
Run the Streamlit dashboard:


streamlit run app.py
📌 Usage
Use the sidebar to filter by team and week.

Yellow rows indicate weeks with at least one back-to-back game for that team.

📝 Notes
Only regular season games are included (no playoffs).

Data is for the 2023-24 NBA season.

To update for a new season, change the SEASON constant in fetch_schedule.py and rerun the scripts.

🐍 Requirements
Python 3.8+

See requirements.txt for full package list.

Enjoy your NBA Fantasy Dashboard! 🏀

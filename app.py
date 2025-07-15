import streamlit as st
import pandas as pd
import os
import altair as alt

# Path to processed data
DATA_PATH = os.path.join('data', 'processed_weekly_games.csv')

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def main():
    st.title('NBA 2023-24 Weekly Team Schedule Dashboard')

    df = load_data()
    teams = sorted(df['TEAM_ABBREVIATION'].unique())
    weeks = sorted(df['WEEK'].unique())

    # Sidebar filter
    st.sidebar.header('Filters')
    week = st.sidebar.selectbox('Select Week', [int(w) for w in weeks])

    # Filter data for selected week
    week_df = df[df['WEEK'] == int(week)]

    # Bar chart: games played per team, color by b2b presence
    week_df['Has_B2B'] = week_df['back_to_backs'] > 0
    chart = alt.Chart(week_df).mark_bar().encode(
        x=alt.X('TEAM_ABBREVIATION:N', title='Team', sort=teams),
        y=alt.Y('games_played:Q', title='Games Played'),
        color=alt.condition(
            alt.datum.Has_B2B,
            alt.value('#ffeb3b'),  # yellow for b2b
            alt.value('#1f77b4')   # blue otherwise
        ),
        tooltip=['TEAM_ABBREVIATION', 'games_played', 'back_to_backs', 'b2b_days']
    ).properties(
        width=700,
        height=400,
        title=f'NBA Games per Team - Week {week}'
    )

    st.altair_chart(chart, use_container_width=True)

    # Show table for reference
    st.subheader(f'Games and Back-to-Backs for Week {week}')
    st.dataframe(
        week_df[['TEAM_ABBREVIATION', 'games_played', 'back_to_backs', 'b2b_days']]
        .sort_values('games_played', ascending=False)
        .reset_index(drop=True),
        use_container_width=True
    )
    st.caption('Yellow bars indicate teams with at least one back-to-back game that week. "b2b_days" shows the days of the week for each back-to-back.')

if __name__ == '__main__':
    main() 
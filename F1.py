import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import numpy as np

# TODO: Show a map with the location of the next/current race
# TODO: Figure out whether an SQLConnection is required
# TODO: Create a connection to a data source or API
# TODO: Convert 2023 excel data to a datasource
# TODO: Streamlit Auth0: create user authentication or Authenticator
# TODO: Snowflake
# https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074
# https://discuss.streamlit.io/t/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/34363

# --- random app ideas to implement later ---
# - text input: let user's submit comments?
# - additional bonus picks for:
#     - DNF driver of the day
#     - Fastest lap pick
#     - I changed my mind pick
# - Guess the fastest lap time with the st.time_input function - closest wins
# - Guess the finish time for the race - closest wins
# - Use file_uploader to allow user's to upload profile pics
# - Use colour_picker to allow user's to pick a colour
# - Create streamlit-lottie animations
# - Add tabs for some sort of race filtering.. not sure if this will work with filtering dataframes
# - Use the st.pydeck_chart to plot a 3Dish sort of map with race locations - interactive somehow??

# ---------------------- SETTINGS ----------------------
race_results = []
page_title = "F1 POLE PREDICTOR"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# --- MAIN APP ---
def main():
    
    # --- Page Info ---
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_icon + " " + page_title + " " + page_icon)
    
    
    # --- Sidebar ---
    st.sidebar.markdown(datetime.today().strftime("%d %b %Y"))
    st.sidebar.text_input("Your name", key="name")
    st.sidebar.text_input("Passowrd", key="password")
    user_name = st.session_state.name
    user_password = st.session_state.password
    st.markdown(" ## Welcome " + user_name + "!")
    
    
    # --- Welcome Container ---
    with st.container(border=True):
        with st.expander("Racing Rules"):
            st.markdown('_Welcome to the F1 Prediction Game! \
                Predict the 10th place driver and earn points._')
        
        actual_result = "Fernando Alonso"
        st.success(f"10th Place: {actual_result}")
    
    # --- Create meetrics ---
    # TODO: Process user guesses somehow...

    # --- Display the actual result (for demo purposes) ---


    # --- Metrics ---
    # TODO: Edit this to show the user's current position and change in position
    with st.container(border=False):
        current_position, current_points, leader_points = st.columns(3)
        current_position.container(height=120).metric("Current Position", 2, 5)
        current_points.container(height=120).metric("Current Points", 98, 12)
        leader_points.container(height=120).metric("Leader Points", 125, 25)

    # --- Show a map ---
    map_container = st.container(border=True)
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])
    map_container.map(df)
    # st.map(df)


    # --- Load data ---
    df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
    df = df.T
    cumulative_points = df.cumsum()

    # --- Plot cumulative points ---
    st.header("Leaderboard")
    
plot_cumulative_points(cumulative_points)


# TODO: Redo this section to convert the results to a dataframe.
def plot_cumulative_points(cumulative_points):
     # Create a new figure
     fig, ax = plt.subplots()

     # Plot cumulative points for each user
     for user in cumulative_points.columns:
         final_points = cumulative_points[user].iloc[-1]
         if final_points >= 180:
             if cumulative_points[user].max() == cumulative_points.max().max():
                 ax.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=3, color='black')
             else:
                 ax.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=2)
         else:
             ax.plot(cumulative_points.index, cumulative_points[user], color='grey', alpha=0.3)

         # Annotate the plot with the name of the leader for each race
         prev_leader = None
         for i, race in enumerate(cumulative_points.index):
             leader = cumulative_points.loc[race].idxmax()
             leader_points = cumulative_points.loc[race, leader]
             if leader != prev_leader:
                 ax.text(i, leader_points + 15, leader, ha='center', va='bottom', fontsize=8, color='black', rotation=0, alpha=0.1)
                 ax.plot([i, i], [leader_points, leader_points + 10], color='black', linestyle='-', linewidth=0.1)
                 prev_leader = leader

     # Set labels and title
     ax.set_xlabel('Race')
     ax.set_ylabel('Leaderboard')
     ax.set_title('Cumulative Points by Race for Each User')
     num_races = 22
     ax.set_xticks(range(num_races))
     ax.set_ylim(0, cumulative_points.max().max()+50)
     plt.xticks(rotation=90)
     ax.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 8}, frameon=False)
     plt.tight_layout()
     ax.grid(color='gray', linestyle='--', linewidth=0.5)

     # Display the plot
     st.pyplot(fig)

# Run the app
if __name__ == "__main__":
    main()

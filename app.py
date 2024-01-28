import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import numpy as np

# ---------------------- SETTINGS ----------------------
race_results = []
driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Sergio Perez",
            "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso",
            "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "Kimi Raikkonen",
            "Antonio Giovinazzi", "George Russell", "Mick Schumacher", "Nikita Mazepin", "Nicholas Latifi")
page_title = "F1 Pole Predictor!"
page_icon = ':racing_car:'
layout = 'centered'
# ------------------------------------------------------

# --- MAIN APP ---
def main():
    # Page Info
    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)
    st.text('Welcome to the F1 Prediction Game! Predict the 10th place driver and earn points.')
    st.markdown(datetime.today().strftime("%d %b %Y"))

    # --- Get user's guess ---
    st.subheader(f'Select your :red[drivers]... ')
    with st.form("entry_form", clear_on_submit=True):
        driver1, driver2 = st.columns(2)
        driver1.selectbox("First Pick:", driver_names, key="driver1")
        driver2.selectbox("Second Pick:", driver_names, key="driver2")
        submitted = st.form_submit_button("Place your bet!")

        if submitted:
            driver1 = st.session_state["driver1"]
            driver2 = st.session_state["driver2"]
            st.success("I can't believe you've done this :0")
            # TODO: update a a database with the user's guess


    # --- Create meetrics ---
    # TODO: Process user guesses somehow...

    # Display the actual result (for demo purposes)
    actual_result = "Fernando Alonso"
    st.info(f"Actual 10th place driver: {actual_result}")

    # Load data
    df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
    df = df.T
    cumulative_points = df.cumsum()

    # Plot cumulative points
    st.header("Cumulative Points")
    plot_cumulative_points(cumulative_points)


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
    ax.set_ylabel('Cumulative Points')
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

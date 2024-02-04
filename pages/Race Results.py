'''
This page reveals the race results. 
# TODO: Figure out how to use ErgastAPI for past race results. 
# TODO: Figure out how to update live race stats. 

For now this page is on its own to figure out how the Ergast API works. 
'''

import streamlit as st
import requests
import pandas as pd

# # --- Sidebar ---
# st.sidebar.markdown("## Last Race Results 🏁")

# # --- Tabs ---
# tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
# tab1.write("This is a tab")
# tab2.write("And another onw!")

# # --- Container ---
# c = st.container(border=True)
# c.markdown("Race Results 🏁")
# c.markdown("Show results")
# st.markdown("# Race Results 🏁")



# # --- Get list of drivers and their stats from the F1 data API
# url = "http://ergast.com/api/f1/2023/last/drivers.json" # this API will be shut down end of 2024 :(
# response = requests.get(url)
# data = response.json()

# # Convert the data to a pandas DataFrame
# drivers = pd.DataFrame(data["MRData"]["DriverTable"]["Drivers"])
# drivers["Name"] = drivers["givenName"] + " " + drivers["familyName"]
# st.dataframe(drivers)



# Define function to fetch race results from Ergast API
def fetch_race_results(season):
    url = f"http://ergast.com/api/f1/{season}/results.json"
    response = requests.get(url)
    data = response.json()
    races = data['MRData']['RaceTable']['Races']
    race_results = []
    for race in races:
        for result in race['Results']:
            result_data = {
                'Position': result['position'],
                'Driver': result['Driver']['givenName'] + ' ' + result['Driver']['familyName'],
                'Final Race Points': result['points'],
                'Number of Pit Stops': result['PitStops'],
                'Circuit Name': race['Circuit']['circuitName'],
                'Location': race['Circuit']['Location']['locality'],
                'Date': race['date'],
                'Season': race['season']
            }
            race_results.append(result_data)
    return pd.DataFrame(race_results)

# Main function to run Streamlit app
def main():
    st.title('Formula 1 Race Results Explorer')

    # Sidebar for user input
    season = st.sidebar.text_input('Enter season (e.g., 2023):', '2022')
    circuits = st.sidebar.multiselect('Select circuits:', ['Monaco', 'Silverstone', 'Monza'])

    # Fetch race results
    race_results_df = fetch_race_results(season)

    # Apply filters
    filtered_results_df = race_results_df[race_results_df['Circuit Name'].isin(circuits)]

    # Show filtered results
    st.write('### Filtered Race Results')
    st.dataframe(filtered_results_df)

# Run the app
if __name__ == '__main__':
    main()



'''
This page reveals the race results. 
# TODO: Figure out how to use ErgastAPI for past race results. 
# TODO: Figure out how to update live race stats. 

For now this page is on its own to figure out how the Ergast API works. 
'''

import streamlit as st
import requests
import pandas as pd

# --- Sidebar ---
st.sidebar.markdown("## Last Race Results 🏁")

# --- Tabs ---
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
tab1.write("This is a tab")
tab2.write("And another onw!")

# --- Container ---
c = st.container(border=True)
c.markdown("Race Results 🏁")
c.markdown("Show results")
st.markdown("# Race Results 🏁")



# --- Get list of drivers and their stats from the F1 data API
url = "http://ergast.com/api/f1/2023/last/drivers.json" # this API will be shut down end of 2024 :(
response = requests.get(url)
data = response.json()

# Convert the data to a pandas DataFrame
drivers = pd.DataFrame(data["MRData"]["DriverTable"]["Drivers"])
drivers["Name"] = drivers["givenName"] + " " + drivers["familyName"]
st.dataframe(drivers)


# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Extract JSON data from the response
#     data = response.json()

#     # Process the JSON data
#     # Here you can access and manipulate the data as needed
#     # For example, you can iterate over the drivers and their stats
#     drivers = data['MRData']['DriverTable']['Drivers']
#     st.text(drivers)
#     for driver in drivers:
#         driver_id = driver['driverId']
#         driver_name = driver['givenName'] + ' ' + driver['familyName']
#         # Access other driver stats as needed
#     st.text("successful")
#     st.text(driver_name)
# else:
#     # Print an error message if the request was not successful
#     print(f"Failed to fetch data. Status code: {response.status_code}")


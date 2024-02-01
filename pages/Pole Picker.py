'''
This page allows the user to select their drivers. 
Stats for drivers picked are revealed once the user's guess has been submitted. 
'''

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime
import numpy as np


driver_names = ("Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Sergio Perez",
            "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso",
            "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "Kimi Raikkonen",
            "Antonio Giovinazzi", "George Russell", "Mick Schumacher", "Nikita Mazepin", "Nicholas Latifi")


# --- Get user's guess ---
st.subheader(f'Select your :red[drivers]... ')
with st.sidebar:
    with st.form("entry_form", clear_on_submit=True):
        driver1 = st.selectbox("First Pick:", driver_names, key="driver1")
        driver2 = st.selectbox("Second Pick:", driver_names, key="driver2")
        submitted = st.form_submit_button("Place your bet!")

        if submitted:
            driver1 = st.session_state["driver1"]
            driver2 = st.session_state["driver2"]
            st.success("I can't believe you've done this :0")
            st.balloons()
            # TODO: update a a database with the user's guess

with st.container(border=True):
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))
   

# --- Show scatterplot of driver picks ---
import plotly.express as px
import streamlit as st

df = px.data.gapminder()

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)
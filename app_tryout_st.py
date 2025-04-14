## to run the streamlit app insert in the console
### streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Services.Energy.energy_calc_service import EnergyCalculations
import app

##Set up page layout
st.set_page_config(layout="wide")
st.title('AkashaCalc - Green House Gases Calculator')

###Sidebar info
st.sidebar.header('Parameters')
#project_phase = st.sidebar.selectbox('Porject Phase', ['Construction Phase', 'Operation Phase', 'All Project'])
ghg_source = st.sidebar.selectbox('GHG Emissions Source', ['Energy', 'Fixed Combustion', 'Mobile Combustion', 'Vehicles' \
    ,'Materials Production', 'Materials Use', 'Soil Use Change', 'Waste Treatment', 'All Emissions'])

if st.sidebar.button('Update'):
    if ghg_source == 'Energy':
        years = list(range(1, len(EnergyCalculations.total_emissions_peryear_energy()) + 1))

        plt.figure(figsize=(10, 6))
        plt.plot(years, EnergyCalculations.total_emissions_peryear_energy(), marker='o', linestyle='-', color='g')

        plt.title('Energy - Cumulative Emissions Over Time')
        plt.xlabel('Year')
        plt.ylabel('Cumulative Emissions (tons of CO2e)')
        plt.grid(True)
        plt.show()
    app.plot_energy_peryear()
    

'''
### WIDGETS
##tables and charts

## Create a simple dataframe + Display the dataframe
df =  pd.DataFrame({
    '1st column': ['a', 'b', 'c'],
    '2nd column': [1, 2, 3]
})

st.write(df)

## Create a linechart + Display the linechart
chart_data = df =  pd.DataFrame (
    np.random.randn(20,3), columns = ['a', 'b', 'c']
    )

st.line_chart(chart_data)

##interative widgets

## User insert free input
project_type = st.text_input("Please enter the title of your project")
if project_type:
    st.write( f"Project {project_type} is starting." )

## Slider input
project_lifetime = st.slider("Please your project lifetime", 0, 50 ,20)
st.write( f"The project lifetime will be considered is {project_lifetime}." )

##Option input
parameters = ["energy balance", "soil use", "vehicles"]
choice = st.selectbox("Please enter the type of your project", parameters)
st.write(f"The type of your project is {choice}")

'''
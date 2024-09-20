## to run the streamlit app insert in the console
### streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np

## App Tittle
st.title("Green House Gases Emissions Calculator")
## Display text
st.write("Developed by Marta Tejada - Instituto Superior Técnico & Aqualogus")

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
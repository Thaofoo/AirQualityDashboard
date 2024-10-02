# prompt: based on all those plot, make simple streamlit dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

dataset = pd.read_csv("https://raw.githubusercontent.com/marceloreis/HTI/refs/heads/master/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv")

st.title("Air Quality Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Temperature Analysis", "Pollutant Trends", "Correlation Analysis"])

if page == "Temperature Analysis":
    st.header("Temperature Analysis")
    avg_temp_by_year = dataset.groupby(by='year')['TEMP'].mean()
    
    st.subheader("Average Temperature by Year")
    st.line_chart(avg_temp_by_year)
    
    st.subheader("Average Temperature (Excluding 2017)")
    avg_temp_by_year_no_2017 = avg_temp_by_year.drop(2017)
    st.line_chart(avg_temp_by_year_no_2017)
    
    st.write("**Insight:** The highest average temperature was recorded in 2013 and the lowest in 2015.")

elif page == "Pollutant Trends":
    st.header("Pollutant Trends")
    avg_co_by_month = dataset.groupby(by=['year', 'month'])[['SO2', 'NO2', 'CO', 'O3']].mean()
    
    st.subheader("Monthly Trends of SO2, NO2, CO, and O3")
    fig, ax = plt.subplots(figsize=(12, 6))
    x_axis = [str(i) for i in avg_co_by_month.index]
    ax.plot(x_axis, avg_co_by_month['SO2'], label='SO2', color='blue')
    ax.plot(x_axis, avg_co_by_month['NO2'], label='NO2', color='red')
    ax.plot(x_axis, avg_co_by_month['O3'], label='O3', color='orange')
    ax.set_xlabel('Year and Month')
    ax.set_ylabel('Average Concentration')
    ax.set_title('Monthly Trend of SO2, NO2, and O3 Concentration in Aotizhongxin')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.write("**Insight:** Pollutant levels show fluctuation patterns each year. O3 shows an upward trend peaking in the middle of the year and then declining towards the end of the year.")
    

elif page == "Correlation Analysis":
    st.header("Correlation Analysis")
    st.subheader("Correlation Matrix")
    correlation = dataset.drop(['wd', 'station'], axis=1).corr()
    st.dataframe(correlation)
    
    st.subheader("Correlation between Temperature and O3 Concentration")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(dataset['TEMP'], dataset['O3'], s=2)
    ax.set_xlabel('Temperature')
    ax.set_ylabel('O3 Concentration')
    ax.set_title('Correlation between Temperature and O3 Concentration')
    ax.grid(True)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(dataset['TEMP'], dataset['O3'])
    ax.plot(dataset['TEMP'], slope * dataset['TEMP'] + intercept, color='red', label='Regression Line')
    
    ax.legend()
    st.pyplot(fig)

    st.write("**Insight:** There's a positive correlation between Temperature and O3 concentration.")



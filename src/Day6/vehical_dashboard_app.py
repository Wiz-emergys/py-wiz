'''
5. Create a Streamlit dashboard using the vehicles.csv datafile that allows users to
explore vehicle data dynamically. Filter the data by car manufacturer.
*Imp - Understand the data and columns present in the data.
1. User should be able to select the car manufacturer with the help of a
select-box
2. Filter the data based on the selected manufacturer and plot 4 types of
graphs.
3. The graphs should be relevant and should make sense.
1. For ex. Plot a scatterplot of Engine size v/s fuel efficiency
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Load data
def load_data():
    file_path = "cars_clus.csv"
    df = pd.read_csv(file_path)
    return df
 
df = load_data()
 
# Streamlit UI
st.set_page_config(page_title="Vehicle Data Dashboard", layout="wide")
st.title("🚗 Vehicle Data Explorer")
 
with st.sidebar:
    st.header("Filter Options")
    manufacturers = df["manufact"].unique()
    selected_manufacturer = st.selectbox("Select a Manufacturer", manufacturers)
 
filtered_df = df[df["manufact"] == selected_manufacturer]
 
st.subheader(f"Data for {selected_manufacturer}")
st.dataframe(filtered_df)
 
col1, col2 = st.columns(2)
 
with col1:
    st.subheader("Engine Size vs. Fuel Efficiency")
    fig, ax = plt.subplots()
    scatter = ax.scatter(filtered_df["engine_s"], filtered_df["mpg"], c=filtered_df["price"], s=filtered_df["horsepow"])
    ax.set_xlabel("Engine Size (L)")
    ax.set_ylabel("Miles per Gallon")
    plt.colorbar(scatter, label="Price ($K)")
    st.pyplot(fig)
 
    st.subheader("Horsepower Variation")
    fig, ax = plt.subplots()
    ax.plot(filtered_df["model"], filtered_df["horsepow"], marker='o', linestyle='-')
    ax.set_xlabel("Car Model")
    ax.set_ylabel("Horsepower")
    plt.xticks(rotation=90)
    st.pyplot(fig)
 
with col2:
    st.subheader("Price Distribution")
    fig, ax = plt.subplots()
    ax.bar(filtered_df["model"], filtered_df["price"], color='skyblue')
    ax.set_xlabel("Car Model")
    ax.set_ylabel("Price ($K)")
    plt.xticks(rotation=90)
    st.pyplot(fig)
 
    st.subheader("Sales Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["sales"], bins=10, color='orange', edgecolor='black')
    ax.set_xlabel("Sales (Units)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
 
st.caption("Data source: cars_clus.csv")
 
 
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(layout="wide")

# Data reading and preparation
df = pd.read_csv("src/dev.csv", sep=";")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp('M')
df["Year"] = df["Date"].dt.year

# Dropdown for year filter
selected_year = st.sidebar.selectbox("Select Year", options=["All"] + sorted(df["Year"].unique().tolist()), index=0)
if selected_year != "All":
    df = df[df["Year"] == selected_year]

# Grouping data by month for the plots
monthly_data = df.groupby("Month").agg({
    "Text Posts": "sum",
    "Video Posts": "sum",
    "Total": "sum",
    "New Users": "sum"
}).reset_index()

# Line chart for monthly post evolution
fig_total_posts = px.line(monthly_data, x="Month", y="Total", title="Monthly Evolution of Posts")
st.plotly_chart(fig_total_posts, use_container_width=True)

# Line chart comparing types of posts
fig_type_posts = px.line(monthly_data, x="Month", y=["Text Posts", "Video Posts"], title="Evolution of Post Types")
st.plotly_chart(fig_type_posts, use_container_width=True)

# Line chart for new users evolution
fig_new_users = px.line(monthly_data, x="Month", y="New Users", title="Evolution of New Users")
st.plotly_chart(fig_new_users, use_container_width=True)

# Stacked bar chart
fig_stacked = px.bar(monthly_data, x="Month", y=["Text Posts", "Video Posts"], title="Proportion of Post Types by Month",
                     labels={"value": "Number of Posts", "variable": "Type of Post"})
st.plotly_chart(fig_stacked, use_container_width=True)

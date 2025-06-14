import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("youtube_data.csv")

st.set_page_config(page_title="YouTube Trending Dashboard", layout="wide")
st.title("📺 YouTube Trending Analytics Dashboard (2024 Edition)")

# Sidebar filters
category_filter = st.sidebar.selectbox("Select Category", ["All"] + sorted(df['category'].unique().tolist()))
if category_filter != "All":
    df = df[df['category'] == category_filter]

# Views by Category
st.subheader("📊 Average Views by Category")
views_chart = df.groupby('category')['views'].mean().reset_index()
fig1 = px.bar(views_chart, x='category', y='views', title='Average Views per Category')
st.plotly_chart(fig1, use_container_width=True)

# Most Liked Videos
st.subheader("🔥 Top 5 Most Liked Videos")
top_liked = df.sort_values(by="likes", ascending=False).head(5)
st.table(top_liked[['title', 'channel', 'likes']])

# Daily Upload Trends
st.subheader("📈 Trending Uploads Over Time")
df['published_at'] = pd.to_datetime(df['published_at'])
time_series = df.groupby(df['published_at'].dt.to_period('M')).size().reset_index(name='uploads')
time_series['published_at'] = time_series['published_at'].astype(str)
fig2 = px.line(time_series, x='published_at', y='uploads', title='Monthly Trending Uploads')
st.plotly_chart(fig2, use_container_width=True)

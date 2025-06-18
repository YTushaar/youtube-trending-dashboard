import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import subprocess

# ---- Streamlit Page Config ----
st.set_page_config(page_title="YouTube Trending Dashboard", layout="wide")
st.title("📺 YouTube Trending Analytics Dashboard")
st.caption("Powered by real-time data via YouTube API")
st.caption(f"Data last fetched: {datetime.date.today()}")

# ---- Optional: Refresh Button ----
if st.sidebar.button("🔄 Refresh YouTube Data"):
    with st.spinner("Fetching fresh trending videos..."):
        subprocess.run(["python", "fetch_data.py"])
    st.success("✅ Data updated! Please refresh the page.")

# ---- Load CSV ----
try:
    df = pd.read_csv("live_youtube_data.csv")
except FileNotFoundError:
    st.error("Data file not found. Please run fetch_data.py first.")
    st.stop()

# ---- Category Mapping ----
category_map = {
    "1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music",
    "15": "Pets & Animals", "17": "Sports", "20": "Gaming",
    "22": "People & Blogs", "23": "Comedy", "24": "Entertainment",
    "25": "News & Politics", "26": "Howto & Style", "27": "Education",
    "28": "Science & Technology"
}
df["category"] = df["category_id"].astype(str).map(category_map).fillna("Other")
df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')

# ---- Sidebar Filters ----
category_filter = st.sidebar.selectbox("🎯 Filter by Category", ["All"] + sorted(df['category'].unique()))
sort_by = st.sidebar.selectbox("📌 Sort Videos By", ["Views", "Likes", "Comments"])
sort_column_map = {
    "Views": "views",
    "Likes": "likes",
    "Comments": "comments"
}
sort_column = sort_column_map[sort_by]

# ---- Filter Data ----
filtered_df = df.copy()
if category_filter != "All":
    filtered_df = filtered_df[filtered_df['category'] == category_filter]

# ---- Average Views by Category ----
st.subheader("📊 Average Views by Category")
if category_filter != "All":
    st.subheader(f"Top Viewed Videos in '{category_filter}'")
    top_views = filtered_df.sort_values(by="views", ascending=False).head(10)
    fig1 = px.bar(top_views, x='title', y='views', color='channel',
                  title=f'Top 10 Most Viewed Videos in {category_filter}',
                  labels={'views': 'Views', 'title': 'Video Title'})
else:
    st.subheader("Average Views by Category")
    views_chart = filtered_df.groupby('category')['views'].mean().reset_index().sort_values(by='views', ascending=False)
    fig1 = px.bar(views_chart, x='category', y='views', title='Average Views per Category')

st.plotly_chart(fig1, use_container_width=True)


# ---- Top Videos by Sort Selection ----
st.subheader(f"🏆 Top Videos in '{category_filter}' by {sort_by}")
if filtered_df.empty:
    st.info("No videos found in this category.")
else:
    top_sorted = filtered_df.sort_values(by=sort_column, ascending=False).head(5)
    st.caption(f"Showing top {min(5, len(filtered_df))} of {len(filtered_df)} video(s)")
    st.dataframe(top_sorted[['title', 'channel', sort_column]], use_container_width=True)

# ---- Monthly Upload Trend ----
st.subheader("📈 Monthly Upload Trend")
monthly_uploads = filtered_df.groupby(filtered_df['published_at'].dt.to_period('M')).size().reset_index(name='uploads')
monthly_uploads['published_at'] = monthly_uploads['published_at'].astype(str)
fig2 = px.line(monthly_uploads, x='published_at', y='uploads', title='Monthly Trending Uploads')
st.plotly_chart(fig2, use_container_width=True)

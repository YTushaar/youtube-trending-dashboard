import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
REGION_CODE = "IN"
MAX_RESULTS = 25

# 🌐 API Endpoint
url = (
    f"https://www.googleapis.com/youtube/v3/videos"
    f"?part=snippet,statistics"
    f"&chart=mostPopular"
    f"&regionCode={REGION_CODE}"
    f"&maxResults={MAX_RESULTS}"
    f"&key={API_KEY}"
)

# 📡 Request
response = requests.get(url)

# ❌ Error check
if response.status_code != 200:
    print("❌ API call failed:", response.status_code)
    exit()

data = response.json()

# 📊 Extract & Format Data
videos = []
for item in data.get("items", []):
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})

    video = {
        "title": snippet.get("title", ""),
        "channel": snippet.get("channelTitle", ""),
        "category_id": str(snippet.get("categoryId", "0")),  # Make sure it's a string
        "published_at": snippet.get("publishedAt", ""),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
    }
    videos.append(video)

# 📁 Save to CSV
df = pd.DataFrame(videos)
df.to_csv("live_youtube_data.csv", index=False)
print("✅ Trending data saved to live_youtube_data.csv")

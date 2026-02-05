import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Pre-defined RSS Feeds
RSS_FEEDS = {
    "tech": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://venturebeat.com/feed/",
        "https://www.wired.com/feed/rss"
    ],
    "crypto": [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/rss",
        "https://decrypt.co/feed",
        "https://thedefiant.io/api/feed",
        "https://www.theblock.co/rss"
    ],
    "ai": [
        "https://www.mit.edu/rss/research.xml",  # MIT Research (often AI)
        "https://blogs.nvidia.com/feed/",
        "https://openai.com/blog/rss.xml",
        "https://www.artificialintelligence-news.com/feed/"
    ],
    "general": [
        # Google News RSS (Dynamic URL generated in code usually, but base here)
        "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    ]
}

# YouTube Configuration
YOUTUBE_SEARCH_LIMIT = 3

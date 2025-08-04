import requests
import urllib.parse
import string
import pandas as pd
import ace_tools as tools
import time

# Define base keyword
base_keyword = "supply chain analytics"

# Function to fetch Google autocomplete suggestions
def fetch_google_suggestions(query):
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(query)}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()[1]
    except:
        return []
    return []

# Expanded keywords for autocomplete generation
expanded_keywords = [f"{base_keyword} {char}" for char in string.ascii_lowercase + string.digits]

# Fetch suggestions
all_suggestions = set()

for kw in expanded_keywords:
    suggestions = fetch_google_suggestions(kw)
    all_suggestions.update(suggestions)
    time.sleep(0.2)  # Respect rate limits

# Select top 100 suggestions
top_100_suggestions = sorted(all_suggestions)[:100]

# Create DataFrame and show
df = pd.DataFrame(top_100_suggestions, columns=["Keyword Suggestion"])
tools.display_dataframe_to_user(name="Top 100 Keyword Suggestions", dataframe=df)

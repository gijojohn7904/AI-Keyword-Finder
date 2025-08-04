import requests
import urllib.parse
import string

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

# Expand the base keyword by appending letters a–z and numbers 0–9
expanded_keywords = [f"{base_keyword} {char}" for char in list(string.ascii_lowercase) + list(map(str, range(10)))]

# Collect all suggestions
all_suggestions = set()

for kw in expanded_keywords:
    suggestions = fetch_google_suggestions(kw)
    if suggestions:
        all_suggestions.update(suggestions)

# Convert to sorted list and limit to 100 ideas
final_suggestions = sorted(list(all_suggestions))[:100]

import pandas as pd
import ace_tools as tools

# Save to DataFrame and display
df = pd.DataFrame(final_suggestions, columns=["Keyword Idea"])
tools.display_dataframe_to_user(name="100 Keyword Ideas", dataframe=df)

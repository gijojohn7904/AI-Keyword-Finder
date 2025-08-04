import streamlit as st
import requests
import pandas as pd
import urllib.parse

# Function to fetch autocomplete suggestions from Google
def fetch_google_suggestions(keyword: str):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(keyword)}"
    response = requests.get(url)
    if response.status_code == 200:
        suggestions = response.json()[1]
        return suggestions
    return []

# Categorize suggestions based on type
def categorize_suggestions(base_keyword, suggestions):
    questions = []
    prepositions = []
    comparisons = []
    a_to_z = []

    for s in suggestions:
        lower = s.lower()
        if any(lower.startswith(q) for q in ["what", "why", "how", "can", "should", "does"]):
            questions.append(s)
        elif any(p in lower for p in [" for ", " with ", " to ", " in "]):
            prepositions.append(s)
        elif any(c in lower for c in [" vs ", " like ", " or "]):
            comparisons.append(s)
        else:
            a_to_z.append(s)

    return questions, prepositions, comparisons, a_to_z

# Streamlit UI
st.title("🔍 AI Keyword Planner v0.1")
st.markdown("Fetch real-time Google keyword suggestions by category")

keyword = st.text_input("Enter a keyword to explore:")

if keyword:
    suggestions = fetch_google_suggestions(keyword)
    if suggestions:
        q, p, c, az = categorize_suggestions(keyword, suggestions)

        tab1, tab2, tab3, tab4 = st.tabs(["❓ Questions", "🔗 Prepositions", "⚖️ Comparisons", "🔤 A–Z"])
        with tab1:
            st.write(q)
        with tab2:
            st.write(p)
        with tab3:
            st.write(c)
        with tab4:
            st.write(az)

        # Export to CSV
        all_data = {"Questions": q, "Prepositions": p, "Comparisons": c, "A-Z Variants": az}
        rows = [{"Category": cat, "Suggestion": val} for cat, vals in all_data.items() for val in vals]
        df = pd.DataFrame(rows)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "ai_keyword_suggestions.csv", "text/csv")
    else:
        st.warning("No suggestions found or rate-limited by Google.")
else:
    st.info("Type a keyword to begin...")

import os
import pandas as pd
import requests
import streamlit as st
import urllib.parse

# Set Streamlit page config
st.set_page_config(page_title="AI Keyword Planner", layout="centered")

st.title("🔍 AI Keyword Planner v0.1")
st.markdown("Get real-time Google autocomplete suggestions. Categorized for easy keyword planning.")

# User input
keyword = st.text_input("Enter a keyword to explore:", placeholder="e.g., supply chain analytics")

def fetch_google_suggestions(base_keyword):
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(base_keyword)}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()[1]
        else:
            return []
    except:
        return []

def categorize_suggestions(base_keyword, suggestions):
    questions, prepositions, comparisons, a_to_z = [], [], [], []
    for s in suggestions:
        l = s.lower()
        if any(l.startswith(q) for q in ["what", "how", "why", "can", "should", "is", "does"]):
            questions.append(s)
        elif any(p in l for p in [" for ", " to ", " with ", " without ", " in "]):
            prepositions.append(s)
        elif any(c in l for c in [" vs ", " like ", " or "]):
            comparisons.append(s)
        else:
            a_to_z.append(s)
    return questions, prepositions, comparisons, a_to_z

if keyword:
    suggestions = fetch_google_suggestions(keyword)
    if suggestions:
        questions, prepositions, comparisons, a_to_z = categorize_suggestions(keyword, suggestions)

        with st.expander("❓ Questions"):
            st.write(questions if questions else "No suggestions found.")
        with st.expander("🔗 Prepositions"):
            st.write(prepositions if prepositions else "No suggestions found.")
        with st.expander("⚖️ Comparisons"):
            st.write(comparisons if comparisons else "No suggestions found.")
        with st.expander("🔤 A–Z Variants"):
            st.write(a_to_z if a_to_z else "No suggestions found.")

        # Prepare for download
        rows = []
        for category, values in {
            "Questions": questions,
            "Prepositions": prepositions,
            "Comparisons": comparisons,
            "A-Z Variants": a_to_z
        }.items():
            for v in values:
                rows.append({"Category": category, "Suggestion": v})

        df = pd.DataFrame(rows)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="keyword_suggestions.csv", mime="text/csv")
    else:
        st.warning("No results from Google. Try a different keyword.")
else:
    st.info("Start typing a keyword to get autocomplete suggestions.")

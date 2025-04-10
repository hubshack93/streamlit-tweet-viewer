import streamlit as st
import json
import random
import os
from datetime import datetime

# Load merged JSON
@st.cache_data
def load_data():
    with open("ahlam.json", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# Ensure tweet list is not empty
if not data:
    st.error("No tweets found in merged_tweets.json")
    st.stop()

# Sort by date if available
def safe_parse_date(tweet):
    try:
        return datetime.strptime(tweet["tweetDate"], "%a %b %d %H:%M:%S %z %Y")
    except:
        return datetime.min

from datetime import timezone

def safe_parse_date(item):
    try:
        dt = datetime.fromisoformat(item.get("tweetDate", ""))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)  # make naive datetime timezone-aware
        return dt
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)

# Session State for navigation
if "index" not in st.session_state:
    st.session_state.index = 0
if "annotations" not in st.session_state:
    st.session_state.annotations = {}

# Layout
st.title("🗂️ Tweet Viewer for Discourse Analysis")
st.markdown("Use this interface to annotate tweets, track silences, and navigate narratives.")

# Show tweet
tweet = data[st.session_state.index]
st.markdown(f"**Tweet {st.session_state.index+1}/{len(data)}**")
st.code(tweet.get("content", "[No content]"), language="markdown")

# Tagging
tag = st.text_input("Add a tag (e.g., grief, support, silencing)", value="")
note = st.text_area("Notes")

if st.button("💾 Save Tag and Note"):
    st.session_state.annotations[st.session_state.index] = {
        "tag": tag,
        "note": note,
        "tweet": tweet
    }
    st.success("Annotation saved!")

# Navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Previous") and st.session_state.index > 0:
        st.session_state.index -= 1
with col2:
    if st.button("🔀 Random"):
        st.session_state.index = random.randint(0, len(data)-1)
with col3:
    if st.button("➡️ Next") and st.session_state.index < len(data)-1:
        st.session_state.index += 1

# Export annotations
if st.button("📤 Export All Annotations"):
    with open("annotations_export.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.annotations, f, ensure_ascii=False, indent=2)
    st.success("Annotations exported to annotations_export.json")
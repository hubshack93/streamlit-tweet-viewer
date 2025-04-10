import streamlit as st
import pandas as pd

# Load tweets
@st.cache_data

def load_data():
    df = pd.read_csv("tweets_arabic.csv", encoding="utf-8-sig")
    df = df.dropna(subset=["content"]).reset_index(drop=True)
    df["Note"] = ""
    df["Tag"] = ""
    df["Important"] = False
    return df

df = load_data()

st.set_page_config(layout="wide")
st.title("🗂️ Tweet Flashcard Viewer")

# Navigation
if "index" not in st.session_state:
    st.session_state.index = 0

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.markdown(f"### Tweet {st.session_state.index+1} of {len(df)}")
    st.markdown(f"**Date:** {df.loc[st.session_state.index, 'tweetDate']}")
    st.markdown(f"**Content:**")
    st.markdown(f"<div style='font-size: 1.2em; padding: 1em; background-color: #f9f9f9; border-radius: 6px;'>{df.loc[st.session_state.index, 'content']}</div>", unsafe_allow_html=True)

    # Inputs
    df.at[st.session_state.index, "Tag"] = st.text_input("🏷️ Tag", value=df.at[st.session_state.index, "Tag"])
    df.at[st.session_state.index, "Note"] = st.text_area("📝 Note", value=df.at[st.session_state.index, "Note"], height=100)
    df.at[st.session_state.index, "Important"] = st.checkbox("⭐ Mark as Important", value=df.at[st.session_state.index, "Important"])

    # Save button
    if st.button("💾 Save Notes & Tags"):
        df.to_csv("tweets_annotated.csv", index=False, encoding="utf-8-sig")
        st.success("Annotations saved!")

# Navigation controls
colL, colC, colR = st.columns(3)
with colL:
    if st.button("⏮️ Previous") and st.session_state.index > 0:
        st.session_state.index -= 1
with colR:
    if st.button("⏭️ Next") and st.session_state.index < len(df) - 1:
        st.session_state.index += 1

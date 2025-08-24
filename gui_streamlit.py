import streamlit as st
from search_engine import smart_answer

st.set_page_config(page_title="Indian GK Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Indian GK Chatbot")
st.write("Ask me about Indian Polity, History, or Geography!")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Your Question:")

if st.button("Ask") and query:
    answer, url = smart_answer(query)
    st.session_state.history.append(("You", query))
    st.session_state.history.append(("Bot", answer))
    if url:
        st.session_state.history.append(("Source", url))

for role, msg in st.session_state.history:
    if role == "You":
        st.markdown(f"**🧑 {msg}**")
    elif role == "Bot":
        st.markdown(f"🤖 {msg}")
    else:
        st.markdown(f"[🔗 Source]({msg})")

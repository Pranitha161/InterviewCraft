import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# Mapping of topic to source URL
topic_urls = {
    "Python": "https://www.geeksforgeeks.org/python-interview-questions/",
    "DBMS": "https://www.geeksforgeeks.org/dbms/commonly-asked-dbms-interview-questions/",
    "Web Development": "https://www.geeksforgeeks.org/html/web-developer-interview-questions-and-answers/",
    "Data Structures": "https://www.geeksforgeeks.org/data-structure-interview-questions/"
}

# Function to scrape questions and model answers
def fetch_questions_and_answers(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        qa_pairs = []
        tags = soup.find_all(["p", "li", "strong", "h2", "h3"])

        for i in range(len(tags)):
            text = tags[i].get_text(strip=True)
            if "?" in text and 5 < len(text) < 200:
                question = text
                answer = tags[i + 1].get_text(strip=True) if i + 1 < len(tags) else "Answer not available."
                qa_pairs.append((question, answer))
        return qa_pairs
    except Exception as e:
        st.error(f"Error while fetching questions: {e}")
        return []

# Streamlit Setup
st.set_page_config(page_title="Smart Interview Practice", layout="centered")
st.title("🧠 Interview Practice")

# Topic Selector
topic = st.selectbox("📘 Select a Topic", list(topic_urls.keys()))

# Session State Initialization
if "prev_topic" not in st.session_state:
    st.session_state.prev_topic = ""
if "qna" not in st.session_state:
    st.session_state.qna = None
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

# Reload question when topic changes
if topic != st.session_state.prev_topic:
    st.session_state.prev_topic = topic
    st.session_state.qna = None
    st.session_state.submitted = False
    st.session_state.user_answer = ""

    with st.spinner("Fetching fresh interview question..."):
        qa_data = fetch_questions_and_answers(topic_urls[topic])
        if qa_data:
            st.session_state.qna = random.choice(qa_data)
        else:
            st.error("Could not load questions for this topic.")

# Main Interaction
if st.session_state.qna:
    q, a = st.session_state.qna
    st.subheader("📌 Question")
    st.info(q)

    st.session_state.user_answer = st.text_area("📝 Your Answer", value=st.session_state.user_answer)

    if not st.session_state.submitted and st.button("✅ Submit"):
        st.session_state.submitted = True

    if st.session_state.submitted:
        st.success("Here's how you did!")
        st.subheader("💡 Model Answer")
        st.markdown(f"**{a}**")

        if st.session_state.user_answer.strip():
            st.subheader("🧠 Your Answer")
            st.write(st.session_state.user_answer)
        else:
            st.warning("Looks like you skipped writing an answer.")
            st.markdown("Use the model response to reflect on how you might approach the question next time. 🚀")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Another Question"):
                qa_data = fetch_questions_and_answers(topic_urls[topic])
                if qa_data:
                    st.session_state.qna = random.choice(qa_data)
                st.session_state.submitted = False
                st.session_state.user_answer = ""
        with col2:
            if st.button("🛑 End Practice"):
                st.session_state.qna = None
                st.session_state.user_answer = ""
                st.session_state.submitted = False
                st.success("✅ Session ended. Come back anytime!")


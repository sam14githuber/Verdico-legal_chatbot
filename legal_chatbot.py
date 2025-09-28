import streamlit as st
import google.generativeai as genai
import os

# -------------------------------
# Setup Gemini API
# -------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDcJXTc_FM2sNqfWrvCrYYsAPKssCPl1AQ")
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.0-flash"
model = genai.GenerativeModel(MODEL_NAME)

# -------------------------------
# Helper Function
# -------------------------------
def get_legal_answer(query, chat_history):
    """
    Sends a legal query to Gemini and returns the answer.
    """
    disclaimer = (
        "You are a legal information assistant. "
        "Provide general legal knowledge only. "
        "Do not give personal legal advice or replace a lawyer."
    )

    prompt = f"{disclaimer}\n\nChat History:\n{chat_history}\n\nUser Query: {query}\n\nAnswer:"

    response = model.generate_content(prompt)
    return response.text

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Legal Chatbot", page_icon="⚖️", layout="wide")
st.title("⚖️ Legal Chatbot")
st.markdown(
    "💡 *This chatbot provides general legal information only. "
    "It is **not a substitute for professional legal advice**.*"
)

# Keep chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""

# Chat input
user_query = st.text_input("Ask your legal question:")

if st.button("Submit") and user_query.strip():
    with st.spinner("Thinking..."):
        answer = get_legal_answer(user_query, st.session_state.chat_history)
        # Update chat history
        st.session_state.chat_history += f"\nUser: {user_query}\nBot: {answer}\n"

    st.subheader("📌 Answer")
    st.write(answer)

# Show past conversation
if st.session_state.chat_history.strip():
    st.subheader("🗂 Chat History")
    st.text(st.session_state.chat_history)

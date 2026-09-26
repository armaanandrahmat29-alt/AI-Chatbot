import streamlit as st
from google import genai
import os  

st.set_page_config(
    page_title="OmniHelper AI - Safe Assistant",
    page_icon="🤝",
    layout="centered"
)

st.title("🤝 Simple Helper AI")
st.write("Ask me anything! I am a safe, family-friendly assistant.")

try:
    render_key = os.environ.get("GOOGLE_API_KEY")
    if not render_key:
        raise ValueError("Key missing in environment")
    client = genai.Client(api_key=render_key)
except Exception as e:
    st.error("Missing GOOGLE_API_KEY. Please add it to your Render Environment Variables!")
    st.stop()

if user_question := st.chat_input("Type your question here..."):
    st.chat_message("user").write(user_question)
   
    safe_rules = (
        "You are OmniHelper, a polite and smart AI assistant. "
        "Answer this question helpfully. CRITICAL SAFETY RULE: Never say anything inappropriate, "
        "harmful, or unsafe. If the user asks for something unsafe, gently decline and offer a safe topic: "
    )
   
    try:
        # UPDATED TO THE CORRECT ACTIVE MODEL VERSION
        ai_answer = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=safe_rules + user_question
        )
        st.chat_message("assistant").write(ai_answer.text)
    except Exception as e:
        st.error(f"Failed to reach AI brain: {e}")

st.write("---")
st.subheader("💼 Want your own custom AI chatbot?")
st.write(
    "Ask me anything "
    "Ai chatbot helper uses O WATER! "
)

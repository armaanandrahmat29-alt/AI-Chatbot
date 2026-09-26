import streamlit as st
from google import genai

# 1. Setup the browser tab name and icon (Search engines read this!)
st.set_page_config(
    page_title="OmniHelper AI - Safe Assistant",
    page_icon="🤝",
    layout="centered"
)

# 2. Setup the web page look
st.title("🤝 Simple Helper AI")
st.write("Ask me anything! I am a safe, family-friendly assistant.")

# 3. Connect to your secret AI key
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Missing GOOGLE_API_KEY. Please add it to your Render Environment Variables!")
    st.stop()

# 4. Create the chat typing box
if user_question := st.chat_input("Type your question here..."):
   
    # Show what you typed
    st.chat_message("user").write(user_question)
   
    # Ask the safe AI brain for the answer with strict safety guidelines
    safe_rules = (
        "You are OmniHelper, a polite and smart AI assistant. "
        "Answer this question helpfully. CRITICAL SAFETY RULE: Never say anything inappropriate, "
        "harmful, or unsafe. If the user asks for something unsafe, gently decline and offer a safe topic: "
    )
   
    try:
        ai_answer = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=safe_rules + user_question
        )
        # Show the AI's answer on the web page
        st.chat_message("assistant").write(ai_answer.text)
    except Exception as e:
        st.error(f"Failed to reach AI brain: {e}")

# 5. Hire Me / Earning Section
st.write("---")
st.subheader("💼 Want your own custom AI chatbot?")
st.write(
    "I am an 11-year-old developer! I can build a customized AI helper just like this "
    "for your local small business or project. Have an adult contact my parents to hire me!"
)

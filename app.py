import streamlit as st
from google import genai

# 1. Setup the web page look
st.title("🤝 Simple Helper AI")
st.write("Ask me anything! I am a safe, family-friendly assistant.")

# 2. Connect to your secret AI key
try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Missing GOOGLE_API_KEY. Please add it to your Streamlit Settings!")
    st.stop()

# 3. Create the chat typing box
if user_question := st.chat_input("Type your question here..."):
   
    # Show what you typed
    st.chat_message("user").write(user_question)
   
    # Ask the safe AI brain for the answer
    safe_rules = "Answer this question helpfully. Never say anything inappropriate or unsafe: "
    ai_answer = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=safe_rules + user_question
    )
   
    # Show the AI's answer on the web page
    st.chat_message("assistant").write(ai_answer.text)

# 4. Hire Me / Earning Section
st.write("---")
st.subheader("💼 Want your own custom AI chatbot?")
st.write("I am an 11-year-old developer! I can build a customized AI helper just like this for your local small business or project. Have an adult contact my parents to hire me!")

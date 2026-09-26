import streamlit as st
from google import genai
from PIL import Image
import os  

# 1. Setup the browser tab name and icon
st.set_page_config(
    page_title="OmniHelper AI - Safe Assistant",
    page_icon="🤝",
    layout="centered"
)

st.title("🤝 OmniHelper AI")
st.write("Ask a question, upload a photo, or get homework help!")

# 2. Reset Chat Button to clear logs instantly
if st.button("🔄 Reset Chat / Clear Memory"):
    st.session_state.messages = []
    st.rerun()

# 3. Connect to your secret AI key using Render's system
try:
    render_key = os.environ.get("GOOGLE_API_KEY")
    if not render_key:
        raise ValueError("Key missing in environment")
    client = genai.Client(api_key=render_key)
except Exception as e:
    st.error("Missing GOOGLE_API_KEY. Please add it to your Render Environment Variables!")
    st.stop()

# 4. Initialize the chat bubble memory bank
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages as bubbles
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. Image Uploader Section
uploaded_file = st.file_uploader("📸 Upload an image or photo for the AI to look at:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image on the screen
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Uploaded Photo", use_container_width=True)

# 6. Chat Input Processing
if user_question := st.chat_input("Type your question here..."):
    # Show user message in a bubble
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})
   
    # Base instructions for safe behavior
    safe_rules = (
        "You are OmniHelper, a polite and smart AI assistant. "
        "Answer this question helpfully. CRITICAL SAFETY RULE: Never say anything inappropriate, "
        "harmful, or unsafe. If the user asks for something unsafe, gently decline and offer a safe topic."
    )
   
    # Gather everything to send to the brain
    contents_to_send = [safe_rules, user_question]
   
    # If the user uploaded a picture, attach it to the message!
    if uploaded_file is not None:
        contents_to_send.append(image)
       
    with st.chat_message("assistant"):
        try:
            ai_answer = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents_to_send
            )
            st.write(ai_answer.text)
            st.session_state.messages.append({"role": "assistant", "content": ai_answer.text})
        except Exception as e:
            st.error("Google's free servers are a bit busy! Click the 'Reset Chat' button at the top to clear the lines and chat instantly.")

# 7. Hire Me / Earning Section
st.write("---")
st.subheader("💼 Want your own custom AI chatbot?")
st.write(
    "Omnibot "
)

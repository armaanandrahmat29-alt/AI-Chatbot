import streamlit as st
import google.generativeai as genai
import os

# Configure the Web Page Layout
st.set_page_config(page_title="no water AI", page_icon="🤖", layout="wide")

# --- SECURE API KEY PIPELINE ---
# Automatically pulls the key you saved in Render's Environment settings
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    # Fallback input box in case it's not set in Render yet
    with st.sidebar:
        st.warning("🔑 Render environment key not detected.")
        GOOGLE_API_KEY = st.text_input("Paste your API Key here manually:", type="password")
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("no water AI 🤖")
    
    # "New Chat" Feature (Clears chat window instantly)
    if st.button("➕ Start New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.rerun()
        
    st.markdown("---")
    
    # Pro Mode Switcher
    is_pro = st.toggle("💎 Activate Pro Mode", value=False)
    
    st.markdown("---")
    
    # File Posting Features (Available on Normal Tier)
    if not is_pro:
        st.subheader("📁 Post Attachments")
        uploaded_file = st.file_uploader("Upload UPD files or Documents", type=["upd", "txt", "pdf", "docx"])
        uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        
        if uploaded_file:
            st.success(f"Successfully posted: {uploaded_file.name}")
        if uploaded_video:
            st.success(f"Successfully posted video: {uploaded_video.name}")
            
        st.info(f"Normal Mode Usage: {st.session_state.message_count} / 30 messages used.")
    else:
        st.success("Premium Pro Active: Unlimited Messages & Advanced AI Help Enabled!")

# --- MAIN CHAT WINDOW ---
st.title("no water AI Interface")

# Display previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle Chat Input
if user_prompt := st.chat_input("Ask no water AI anything..."):
    
    if not is_pro and st.session_state.message_count >= 30:
        st.error("⚠️ You have reached your 30-message limit on the Normal version! Turn on 'Activate Pro Mode' in the sidebar.")
    elif not GOOGLE_API_KEY:
        st.error("⚠️ Missing API Key! Please configure your GOOGLE_API_KEY environment variable on Render.")
    else:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Call the live AI model
        with st.chat_message("assistant"):
            try:
                # Utilizing the fast and capable gemini-2.5-flash model
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                # Pro mode alters the behavior instructions for advanced logic
                if is_pro:
                    full_prompt = f"System Command: You are operating in a highly advanced, expert reasoning mode. Give a master-level solution. User Prompt: {user_prompt}"
                else:
                    st.session_state.message_count += 1
                    full_prompt = user_prompt
                
                response = model.generate_content(full_prompt)
                ai_reply = response.text
                
            except Exception as e:
                ai_reply = f"Error communicating with AI Engine: {str(e)}"
                
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        if not is_pro:
            st.rerun()

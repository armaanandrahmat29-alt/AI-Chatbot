import streamlit as st
import google.generativeai as genai
import os

# Configure the Web Page Layout
st.set_page_config(page_title="no water AI", page_icon="🤖", layout="wide")

# --- CUSTOM CSS THEME (Matches this chat layout) ---
st.markdown("""
    <style>
        /* Main background matching the deep chat canvas */
        .stApp {
            background-color: #0b0f19 !important;
            color: #f3f4f6 !important;
        }
        
        /* Sidebar background styling */
        section[data-testid="stSidebar"] {
            background-color: #030712 !important;
            border-right: 1px solid #1f2937;
        }
        
        /* Text styling inside the sidebar */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label {
            color: #d1d5db !important;
        }
        
        /* Custom Chat Containers */
        .chat-container {
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 16px;
            display: flex;
            align-items: flex-start;
            gap: 16px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Deep background panel for responses */
        .bot-box {
            background-color: #111827 !important;
        }
        
        /* Dark transparent panel for user queries */
        .user-box {
            background-color: rgba(17, 24, 39, 0.4) !important;
        }

        /* Red User Icon Badge */
        .user-avatar {
            background-color: #dc2626;
            color: white;
            border-radius: 8px;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            flex-shrink: 0;
        }

        /* Orange/Amber Assistant Icon Badge */
        .bot-avatar {
            background-color: #ea580c;
            color: white;
            border-radius: 8px;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            flex-shrink: 0;
        }

        .chat-text {
            color: #e5e7eb !important;
            font-size: 15px;
            line-height: 1.6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Clean look for file download fields & buttons */
        div.stButton > button {
            background-color: #1f2937 !important;
            color: white !important;
            border: 1px solid #374151 !important;
            border-radius: 8px !important;
        }
        div.stButton > button:hover {
            border-color: #ea580c !important;
            color: #ea580c !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SECURE API KEY PIPELINE ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
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
    
    # "New Chat" Feature
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
            st.success(f"Posted file: {uploaded_file.name}")
        if uploaded_video:
            st.success(f"Posted video: {uploaded_video.name}")
            
        st.info(f"Normal Mode Usage: {st.session_state.message_count} / 30 messages used.")
    else:
        st.success("Premium Pro Active: Unlimited Messages & Advanced Help Mode.")

# --- MAIN CHAT WINDOW ---
st.title("no water AI")

# Display custom styled conversation blocks
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="chat-container user-box">
                <div class="user-avatar">U</div>
                <div class="chat-text">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-container bot-box">
                <div class="bot-avatar">🤖</div>
                <div class="chat-text">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# Handle Chat Input Box
if user_prompt := st.chat_input("Ask no water AI anything..."):
    
    if not is_pro and st.session_state.message_count >= 30:
        st.error("⚠️ You have reached your 30-message limit on the Normal version! Turn on 'Activate Pro Mode' in the sidebar.")
    elif not GOOGLE_API_KEY:
        st.error("⚠️ Missing API Key! Set up GOOGLE_API_KEY on your Render environment variables dashboard.")
    else:
        # Save user message and render instantly with styled layout
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.markdown(f"""
            <div class="chat-container user-box">
                <div class="user-avatar">U</div>
                <div class="chat-text">{user_prompt}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Pull response from live Gemini Core
        try:
            # Updated to the current active model version
            model = genai.GenerativeModel("gemini-3.8-flash")
            
            if is_pro:
                full_prompt = f"System Command: You are operating in a highly advanced, expert reasoning mode. Give a master-level solution. User Prompt: {user_prompt}"
            else:
                st.session_state.message_count += 1
                full_prompt = user_prompt
            
            response = model.generate_content(full_prompt)
            ai_reply = response.text
            
        except Exception as e:
            ai_reply = f"Error communicating with AI Engine: {str(e)}"
            
        # Save and render assistant reply block
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.markdown(f"""
            <div class="chat-container bot-box">
                <div class="bot-avatar">🤖</div>
                <div class="chat-text">{ai_reply}</div>
            </div>
        """, unsafe_allow_html=True)
            
        if not is_pro:
            st.rerun()

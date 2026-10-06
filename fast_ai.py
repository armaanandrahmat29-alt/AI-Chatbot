import streamlit as st
import google.generativeai as genai
import os

# Configure the Web Page Layout
st.set_page_config(page_title="no water AI", page_icon="🤖", layout="wide")

# --- CUSTOM CSS THEME (Matches this chat layout) ---
st.markdown("""
    <style>
        .stApp { background-color: #0b0f19 !important; color: #f3f4f6 !important; }
        section[data-testid="stSidebar"] { background-color: #030712 !important; border-right: 1px solid #1f2937; }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label { color: #d1d5db !important; }
        .chat-container { border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; display: flex; align-items: flex-start; gap: 16px; border: 1px solid rgba(255, 255, 255, 0.05); }
        .bot-box { background-color: #111827 !important; }
        .user-box { background-color: rgba(17, 24, 39, 0.4) !important; }
        .user-avatar { background-color: #dc2626; color: white; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; flex-shrink: 0; }
        .bot-avatar { background-color: #ea580c; color: white; border-radius: 8px; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; flex-shrink: 0; }
        .chat-text { color: #e5e7eb !important; font-size: 15px; line-height: 1.6; font-family: sans-serif; }
        div.stButton > button { background-color: #1f2937 !important; color: white !important; border: 1px solid #374151 !important; border-radius: 8px !important; }
        div.stButton > button:hover { border-color: #ea580c !important; color: #ea580c !important; }
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
    
    if st.button("➕ Start New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.rerun()
        
    st.markdown("---")
    is_pro = st.toggle("💎 Activate Pro Mode", value=False)
    st.markdown("---")
    
    if not is_pro:
        st.subheader("📁 Post Attachments")
        uploaded_file = st.file_uploader("Upload UPD files or Documents", type=["upd", "txt", "pdf", "docx"])
        uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        
        if uploaded_file: st.success(f"Posted file: {uploaded_file.name}")
        if uploaded_video: st.success(f"Posted video: {uploaded_video.name}")
            
        st.info(f"Normal Mode Usage: {st.session_state.message_count} / 30 messages used.")
    else:
        st.success("Premium Pro Active: Unlimited Messages & Advanced Help Mode.")

# --- MAIN CHAT WINDOW ---
st.title("no water AI")

# Display historical conversation blocks
for msg in st.session_state.messages:
    box_class = "user-box" if msg["role"] == "user" else "bot-box"
    avatar = "U" if msg["role"] == "user" else "🤖"
    avatar_class = "user-avatar" if msg["role"] == "user" else "bot-avatar"
    
    st.markdown(f"""
        <div class="chat-container {box_class}">
            <div class="{avatar_class}">{avatar}</div>
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
        # Save and print user message instantly
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.markdown(f"""
            <div class="chat-container user-box">
                <div class="user-avatar">U</div>
                <div class="chat-text">{user_prompt}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Prepare Streaming Generator function for real-time printing
        def stream_ai_response():
            try:
                model = genai.GenerativeModel("gemini-3.8-flash")
                if is_pro:
                    full_prompt = f"System Command: You are operating in a highly advanced, expert reasoning mode. Give a master-level solution. User Prompt: {user_prompt}"
                else:
                    global message_counter_increment
                    full_prompt = user_prompt
                
                # Using stream=True allows words to fly in instantly 
                response = model.generate_content(full_prompt, stream=True)
                for chunk in response:
                    yield chunk.text
            except Exception as e:
                yield f"Error communicating with AI Engine: {str(e)}"

        # Render incoming response live inside our themed UI
        if not is_pro:
            st.session_state.message_count += 1

        # Use empty placeholder blocks to stream raw text safely inside our CSS HTML structures
        st.markdown('<div class="chat-container bot-box"><div class="bot-avatar">🤖</div><div class="chat-text">', unsafe_allow_html=True)
        full_reply = st.write_stream(stream_ai_response)
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Save full string output into session history 
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
        
        if not is_pro:
            st.rerun()

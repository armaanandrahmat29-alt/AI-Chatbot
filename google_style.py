import streamlit as st
import google.generativeai as genai
import os

# Configure the Web Page Layout
st.set_page_config(page_title="no water AI", page_icon="🤖", layout="wide")

# --- EXACT INTERFACE REPLICATION CSS ---
st.markdown("""
    <style>
        /* Base page background canvas matching your screenshot */
        .stApp {
            background-color: #1e1f20 !important;
            color: #e3e3e3 !important;
        }
        
        /* Ultra-narrow sidebar for the iconic left-rail menu icons */
        section[data-testid="stSidebar"] {
            background-color: #131314 !important;
            border-right: none !important;
            width: 80px !important;
            min-width: 80px !important;
            max-width: 80px !important;
        }
        
        /* Hide sidebar structural wrappers to keep layout tight */
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            padding-top: 2rem !important;
            gap: 1.5rem !important;
        }

        /* Clean native Chat Rows without redundant padding */
        div[data-testid="stChatMessage"] {
            background-color: transparent !important;
            padding: 1.5rem 2rem !important;
            max-width: 850px;
            margin: 0 auto;
        }

        /* Custom User text and bubble formatting */
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] span:contains("user")) {
            color: #e3e3e3 !important;
        }
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] span:contains("user")) div[data-testid="stChatMessageAvatar"] {
            background-color: #3b82f6 !important; /* Clean Blue Profile dot */
            color: white !important;
        }

        /* Custom AI Response styling */
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] span:contains("assistant")) {
            color: #e3e3e3 !important;
        }
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] span:contains("assistant")) div[data-testid="stChatMessageAvatar"] {
            background-color: #ea580c !important; /* Orange branding dot */
            color: white !important;
        }

        /* Round Pill Chat Input Box matching the screen exactly */
        div[data-testid="stChatInput"] {
            background-color: #282a2c !important;
            border-radius: 32px !important;
            border: 1px solid #444746 !important;
            max-width: 850px;
            margin: 0 auto !important;
            padding: 4px 12px !important;
        }
        
        div[data-testid="stChatInput"] textarea {
            color: #e3e3e3 !important;
            background-color: transparent !important;
        }

        /* Styled Action Buttons inside the Sidebar menu */
        div.stButton > button {
            background-color: #282a2c !important;
            color: #e3e3e3 !important;
            border: 1px solid #444746 !important;
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 18px !important;
        }
        div.stButton > button:hover {
            border-color: #ea580c !important;
            color: #ea580c !important;
            background-color: #333537 !important;
        }
        
        /* Wipe default platform headers/footers completely */
        footer {visibility: hidden; height: 0px;}
        header {visibility: hidden; height: 0px;}
        div[data-testid="stStatusWidget"] {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- SECURE API KEY PIPELINE ---
API_KEY_SOURCE = os.environ.get("GOOGLE_API_KEY")

if API_KEY_SOURCE:
    genai.configure(api_key=API_KEY_SOURCE)
else:
    with st.sidebar:
        st.caption("🔒 Key Missing")
        API_KEY_SOURCE = st.text_input("Key:", type="password", label_visibility="collapsed")
        if API_KEY_SOURCE:
            genai.configure(api_key=API_KEY_SOURCE)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# --- MINI SIDEBAR BAR ACTIONS ---
with st.sidebar:
    # Button 1: Reset Chat (Plus sign inside a round button context)
    if st.button("➕", help="Start New Chat", key="new_chat_action"):
        st.session_state.messages = []
        st.session_state.message_count = 0
        st.sidebar.success("Reset")
        st.rerun()

    # Button 2: Toggle Pro Tier (Diamond option)
    is_pro = st.toggle("💎", value=False, help="Toggle Pro Tier Mode")
    
    # Simple constraints tracking panel
    if not is_pro:
        st.caption(f"📝 {st.session_state.message_count}/30")
        # Lightweight doc posting slots
        uploaded_doc = st.file_uploader("📁", type=["upd", "txt", "pdf", "docx"], label_visibility="collapsed")
        if uploaded_doc:
            st.toast(f"Attached: {uploaded_doc.name}")
    else:
        st.caption("💎 Unlimited")

# --- MAIN APP LAYOUT ---
st.markdown("<h2 style='text-align: center; color: #e3e3e3; font-weight: 500; font-family: sans-serif; margin-bottom: 2rem;'>no water AI</h2>", unsafe_allow_html=True)

# Print previous conversation streams with zero visual lag
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capture user text inputs smoothly
if user_prompt := st.chat_input("Ask no water AI..."):
    
    if not is_pro and st.session_state.message_count >= 30:
        st.error("⚠️ Message limit reached on the Normal tier! Toggle Pro Mode in the left menu sidebar.")
    elif not API_KEY_SOURCE:
        st.error("⚠️ Setup your cloud environment API key to submit messages.")
    else:
        # Paint user text row instantly 
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Load backend logic directly for rapid rendering execution
        with st.chat_message("assistant"):
            try:
                engine = genai.GenerativeModel("gemini-3.8-flash")
                
                if is_pro:
                    runtime_prompt = f"System Instruction: Provide an expert, deep-reasoning response. User Prompt: {user_prompt}"
                else:
                    st.session_state.message_count += 1
                    runtime_prompt = user_prompt
                
                # Direct block delivery stops screen stuttering and lag
                response = engine.generate_content(runtime_prompt)
                ai_reply = response.text
                
            except Exception as e:
                ai_reply = f"System processing conflict: {str(e)}"
                
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        if not is_pro:
            st.rerun()

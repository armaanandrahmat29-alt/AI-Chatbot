import streamlit as st

# Configure the Web Page Layout
st.set_page_config(page_title="no water AI", page_icon="🤖", layout="wide")

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
    
    # File Posting Features
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

# Render previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle Chat Input
if user_prompt := st.chat_input("Ask no water AI anything..."):
    
    if not is_pro and st.session_state.message_count >= 30:
        st.error("⚠️ You have reached your 30-message limit on the Normal version! Turn on 'Activate Pro Mode' in the sidebar.")
    else:
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.chat_message("assistant"):
            if is_pro:
                ai_reply = f"**[Advanced Pro Engine]:** Deeply evaluated your prompt. Here is your complex, unlimited assistance logic matching your request for: *'{user_prompt}'*."
            else:
                st.session_state.message_count += 1
                ai_reply = f"This is a standard helpful answer to your prompt: *'{user_prompt}'*."
                
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        if not is_pro:
            st.rerun()

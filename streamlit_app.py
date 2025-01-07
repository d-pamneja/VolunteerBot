import streamlit as st
import requests

st.set_page_config(page_title="Volunteer Assistant", layout="wide")

st.markdown("""
    <style>
    .stTextInput > div { padding: 5px; }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .user-message, .bot-message {
        color: black; /* Text color for both user and bot messages */
        font-family: Arial, sans-serif;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .user-message {
        background-color: #e6f3ff;
    }
    .bot-message {
        background-color: #f0f0f0;
    }
    .chat-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .fixed-buttons {
        position: fixed;
        bottom: 10px;
        width: 90%;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<div class='chat-title'>🤖 Volunteer Assistant</div>", unsafe_allow_html=True)
st.markdown("Welcome! I'm here to help you with the volunteering process. Feel free to ask me anything!")


if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""<div class="user-message"><strong>You:</strong> {message["content"]}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="bot-message"><strong>Assistant:</strong> {message["content"]}</div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='fixed-buttons'>", unsafe_allow_html=True)
user_input = st.text_input("Type your message here:", key="user_input")

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Send") and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        user_input = ""
        
        try:
            response = requests.post(
                "http://localhost:8080/aimind/chat",
                json={"user_query": user_input},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                bot_response = response.json()["response"]
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to the server: {str(e)}")
        
        st.rerun()

with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

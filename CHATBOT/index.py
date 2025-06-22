import streamlit as st
import time
import hashlib
from datetime import datetime

class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! What can I help you with?",
            "how are you": "I'm just a program, but I'm functioning as expected!",
            "bye": "Goodbye! Have a great day!",
            "what is your name": "I am a rule-based chatbot built with Python.",
            "help": "Sure, I can help. Ask me about greetings, my name, or say goodbye.",
            "what can you do": "I can help answer basic questions, provide greetings, and engage in simple conversation. Try asking me 'how are you' or 'what is your name'!",
            "thank you": "You're welcome! Let me know if you need anything else.",
            "good morning": "Good morning! How can I brighten your day?",
            "good evening": "Good evening! How may I assist you tonight?"
        }

    def respond(self, message):
        message = message.lower().strip()
        for pattern in self.rules:
            if pattern in message:
                return self.rules[pattern]
        return "I'm not sure how to respond to that. Try saying 'help' or 'what can you do'."

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def login_page():
    st.markdown("""
    <style>
        /* Modern login form styling */
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
        }
        .stButton > button {
            border-radius: 10px;
            width: 100%;
        }
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .login-container {
                background: #2b2b2b;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.title("👋 Welcome!")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login"):
            if username and password:  # Simple validation - you might want to add more secure validation
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Please enter both username and password")
        st.markdown('</div>', unsafe_allow_html=True)

def chat_interface():
    st.markdown("""
    <style>
        /* Modern chat interface styling */
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Chat message styling */
        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 1rem 0;
        }
        .user-message > div {
            background: linear-gradient(135deg, #00B2FF 0%, #006AFF 100%);
            color: white;
            border-radius: 20px 20px 0 20px;
            padding: 12px 18px;
            max-width: 70%;
            margin-left: 30%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .assistant-message {
            display: flex;
            justify-content: flex-start;
            margin: 1rem 0;
        }
        .assistant-message > div {
            background: #f0f2f6;
            border-radius: 20px 20px 20px 0;
            padding: 12px 18px;
            max-width: 70%;
            margin-right: 30%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Input container styling */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 1rem;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .stTextInput > div > div > input {
            border-radius: 25px;
            padding: 0.5rem 1rem;
            border: 2px solid #eee;
        }
        
        .send-button {
            border-radius: 50%;
            width: 40px;
            height: 40px;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #00B2FF 0%, #006AFF 100%);
            border: none;
            color: white;
            cursor: pointer;
        }
        
        /* Header styling */
        .chat-header {
            padding: 1rem;
            background: white;
            border-bottom: 1px solid #eee;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #666;
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .input-container, .chat-header {
                background: #1e1e1e;
            }
            .assistant-message > div {
                background: #2d2d2d;
                color: #fff;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Chat header
    st.markdown(
        f"""
        <div class="chat-header">
            <div class="user-info">
                <span>👤 {st.session_state.username}</span>
                <span>•</span>
                <span>{datetime.now().strftime('%I:%M %p')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add padding to prevent content from being hidden behind fixed header
    st.markdown("<div style='height: 70px'></div>", unsafe_allow_html=True)

    # Initialize chatbot if not already initialized
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = RuleBasedChatbot()

    # Chat container
    chat_container = st.container()

    # Add padding to prevent content from being hidden behind fixed input
    st.markdown("<div style='height: 80px'></div>", unsafe_allow_html=True)
    
    # Input container at the bottom
    with st.container():
        cols = st.columns([8, 1])
        with cols[0]:
            user_input = st.text_input(
                "Type your message...",
                key=f"user_input_{st.session_state.input_key}",
                label_visibility="collapsed"
            )
        with cols[1]:
            send_button = st.button("➤", key=f"send_{st.session_state.input_key}")

    # Process input
    if user_input and (send_button or True):
        st.session_state.chat_history.append(("user", user_input))
        response = st.session_state.chatbot.respond(user_input)
        st.session_state.chat_history.append(("assistant", response))
        st.session_state.input_key += 1
        st.rerun()

    # Display chat history with custom styling
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(
                    f'''
                    <div class="user-message">
                        <div>{message}</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'''
                    <div class="assistant-message">
                        <div>{message}</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

def main():
    st.set_page_config(
        page_title="Modern AI Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    initialize_session_state()

    if not st.session_state.authenticated:
        login_page()
    else:
        chat_interface()

if __name__ == "__main__":
    main()

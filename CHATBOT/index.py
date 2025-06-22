import streamlit as st
import time
from datetime import datetime

class RuleBasedChatbot:
    def __init__(self, name="AI Assistant"):
        self.name = name
        self.rules = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! What can I help you with?",
            "how are you": "I'm just a program, but I'm functioning as expected!",
            "bye": "Goodbye! Have a great day!",
            "what is your name": f"I am {name}, your friendly AI assistant.",
            "help": "Sure, I can help. Ask me about greetings, my name, or say goodbye.",
            "what can you do": "I can help answer basic questions, provide greetings, and engage in simple conversation. Try asking me 'how are you' or 'what is your name'!",
            "thank you": "You're welcome! Let me know if you need anything else.",
            "good morning": "Good morning! How can I brighten your day?",
            "good evening": "Good evening! How may I assist you tonight?"
        }

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None
    if 'messages_sent' not in st.session_state:
        st.session_state.messages_sent = 0

def show_sidebar():
    with st.sidebar:
        st.title("User Profile")
        st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #f8f9fa;
                padding: 1rem;
            }
            .user-profile {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .stat-card {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="user-profile">', unsafe_allow_html=True)
        st.image("https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y", width=100)
        st.header(f"👤 {st.session_state.username}")
        st.markdown(f"**Login time:** {st.session_state.login_time.strftime('%I:%M %p')}")
        
        st.subheader("Session Stats")
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Messages Sent", st.session_state.messages_sent)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Logout", type="primary"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def login_page():
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.title("👋 Welcome!")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login"):
            if username and password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.login_time = datetime.now()
                st.session_state.messages_sent = 0
                st.rerun()
            else:
                st.error("Please enter both username and password")
        st.markdown('</div>', unsafe_allow_html=True)

def chat_interface():
    st.markdown("""
    <style>
        .chat-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 1rem;
        }
        .message-container {
            margin: 1rem 0;
        }
        .username {
            font-size: 0.8rem;
            margin-bottom: 0.2rem;
            color: #666;
        }
        .user-message {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        .user-message .message {
            background: linear-gradient(135deg, #00B2FF 0%, #006AFF 100%);
            color: white;
            border-radius: 20px 20px 0 20px;
            padding: 12px 18px;
            max-width: 70%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .assistant-message {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .assistant-message .message {
            background: #f0f2f6;
            border-radius: 20px 20px 20px 0;
            padding: 12px 18px;
            max-width: 70%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .chat-header {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .input-area {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            margin-top: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize chatbot if not already initialized
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = RuleBasedChatbot()

    show_sidebar()

    # Main chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Chat header
    st.markdown("""
        <div class="chat-header">
            <h2>💬 Chat Session</h2>
            <p>Chatting with {}</p>
        </div>
    """.format(st.session_state.chatbot.name), unsafe_allow_html=True)

    # Chat messages
    chat_container = st.container()
    
    # Input area
    with st.container():
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        cols = st.columns([8, 1])
        with cols[0]:
            user_input = st.text_input(
                "Type your message...",
                key=f"user_input_{st.session_state.input_key}",
                label_visibility="collapsed"
            )
        with cols[1]:
            send_button = st.button("Send", key=f"send_{st.session_state.input_key}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Process input
    if user_input and (send_button or True):
        st.session_state.chat_history.append(("user", user_input))
        response = st.session_state.chatbot.respond(user_input)
        st.session_state.chat_history.append(("assistant", response))
        st.session_state.messages_sent += 1
        st.session_state.input_key += 1
        st.rerun()

    # Display chat history
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"""
                    <div class="message-container user-message">
                        <div class="username">{st.session_state.username}</div>
                        <div class="message">{message}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="message-container assistant-message">
                        <div class="username">{st.session_state.chatbot.name}</div>
                        <div class="message">{message}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Modern AI Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    initialize_session_state()

    if not st.session_state.authenticated:
        login_page()
    else:
        chat_interface()

if __name__ == "__main__":
    main()

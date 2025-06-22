import streamlit as st
import time

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
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = RuleBasedChatbot()

def main():
    st.set_page_config(
        page_title="AI Chatbot",
        page_icon="🤖",
        layout="wide"
    )

    st.title("🤖 AI Assistant")
    
    # Custom CSS for chat alignment
    st.markdown("""
    <style>
        /* Chat container styling */
        .stChatMessage {
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 0.5rem;
        }
        
        /* User message styling - right align */
        .user-message {
            display: flex;
            justify-content: flex-end;
        }
        .user-message > div {
            background-color: #2e7bf6;
            color: white;
            border-radius: 20px 20px 0 20px;
            padding: 10px 15px;
            max-width: 70%;
            margin-left: 30%;
        }
        
        /* Assistant message styling - left align */
        .assistant-message {
            display: flex;
            justify-content: flex-start;
        }
        .assistant-message > div {
            background-color: #f0f2f6;
            border-radius: 20px 20px 20px 0;
            padding: 10px 15px;
            max-width: 70%;
            margin-right: 30%;
        }
        
        /* Input container styling */
        div.stButton > button {
            width: 100%;
            border-radius: 20px;
        }
        .stTextInput > div > div > input {
            border-radius: 20px;
        }
        
        div[data-testid="stVerticalBlock"] > div:has(div.stChatMessage) {
            padding: 0 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    initialize_session_state()
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = RuleBasedChatbot()

    # Create a container for the chat messages with some padding
    chat_container = st.container()
    
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
            send_button = st.button("Send", key=f"send_{st.session_state.input_key}")

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
                st.markdown(f'<div class="user-message"><div>{message}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message"><div>{message}</div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

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

    # Custom CSS for better UI
    st.markdown("""
    <style>
        div.stButton > button {
            width: 100%;
            border-radius: 20px;
        }
        .stTextInput > div > div > input {
            border-radius: 20px;
        }
        div.css-1p1nwyz.e1tzin5v0 {
            padding: 1rem;
            border-radius: 10px;
            background-color: #f0f2f6;
        }
        div.stChatMessage {
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create three columns for layout
    left_col, main_col, right_col = st.columns([1, 3, 1])

    with main_col:
        st.title("🤖 AI Assistant")
        
        # Chat container with fixed height and scrolling
        chat_placeholder = st.container()
        
        # Add some spacing
        st.markdown("<br>" * 2, unsafe_allow_html=True)
        
        # Input container at the bottom
        input_container = st.container()

        with input_container:
            cols = st.columns([8, 1])
            with cols[0]:
                user_input = st.text_input(
                    "Type your message...",
                    key=f"user_input_{st.session_state.input_key}",
                    label_visibility="collapsed"
                )
            with cols[1]:
                send_button = st.button("➤", key=f"send_{st.session_state.input_key}")

        # Display chat history in the chat container
        with chat_placeholder:
            for role, message in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(message)

        # Process input
        if user_input and (send_button or True):
            st.session_state.chat_history.append(("user", user_input))
            response = st.session_state.chatbot.respond(user_input)
            st.session_state.chat_history.append(("assistant", response))
            st.session_state.input_key += 1
            st.rerun()

if __name__ == "__main__":
    initialize_session_state()
    main()

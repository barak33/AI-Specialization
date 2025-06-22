import streamlit as st

class RuleBasedChatbot:
    def __init__(self):
        self.rules = {
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! What can I help you with?",
            "how are you": "I'm just a program, but I'm functioning as expected!",
            "bye": "Goodbye! Have a great day!",
            "what is your name": "I am a rule-based chatbot built with Python.",
            "help": "Sure, I can help. Ask me about greetings, my name, or say goodbye."
        }

    def respond(self, message):
        message = message.lower().strip()
        for pattern in self.rules:
            if pattern in message:
                return self.rules[pattern]
        return "I'm not sure how to respond to that. Try saying 'help'."

def main():
    st.title("Simple Rule-Based Chatbot")
    st.write("Welcome! Type a message and press Enter to chat.")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    chatbot = RuleBasedChatbot()

    # Get user input
    user_input = st.text_input("You:", key="user_input")

    # Process user input
    if user_input:
        response = chatbot.respond(user_input)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

    # Display chat history
    for role, message in st.session_state.chat_history:
        if role == "You":
            st.write(f"👤 You: {message}")
        else:
            st.write(f"🤖 Bot: {message}")

if __name__ == "__main__":
    main()

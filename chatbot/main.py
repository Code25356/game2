"""Main entry point for the chatbot application."""
from chatbot.ui.chat_window import ChatWindow

def main():
    app = ChatWindow()
    app.run()

if __name__ == "__main__":
    main()

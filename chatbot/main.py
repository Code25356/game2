"""Main entry point for the chatbot application."""
from ui.chat_window import ChatWindow

def main():
    app = ChatWindow()
    app.run()

if __name__ == "__main__":
    main()
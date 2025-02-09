"""Main chat window implementation."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
import threading

from .settings import SettingsDialog
from ..utils.config import Config
from ..services.openai_service import OpenAIService, OpenAIServiceError

class ChatWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config = Config()
        self.title("AI Chatbot")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Initialize OpenAI service if API key is available
        api_key = self.config.get_api_key()
        self.openai_service = OpenAIService(api_key) if api_key else None

        # Track if a request is in progress
        self.is_processing = False

        self._create_menu()
        self._create_widgets()
        self._setup_bindings()

        # Configure tags for chat history
        self.chat_history.tag_configure("user", foreground="blue")
        self.chat_history.tag_configure("bot", foreground="green")
        self.chat_history.tag_configure("error", foreground="red")

    def _create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self._show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def _create_widgets(self):
        """Create and arrange the main window widgets."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Chat history area
        self.chat_history = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=('TkDefaultFont', 10)
        )
        self.chat_history.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.chat_history.config(state=tk.DISABLED)

        # Input area frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        input_frame.grid_columnconfigure(0, weight=1)

        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(
            input_frame,
            textvariable=self.message_var,
            font=('TkDefaultFont', 10)
        )
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))

        # Loading indicator
        self.loading_label = ttk.Label(input_frame, text="Processing...", style="Loading.TLabel")
        self.loading_label.grid(row=0, column=1, padx=(0, 5))
        self.loading_label.grid_remove()  # Hide initially

        # Send button
        self.send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self._send_message
        )
        self.send_button.grid(row=0, column=2, sticky=(tk.E))

        # Configure loading label style
        style = ttk.Style()
        style.configure("Loading.TLabel", foreground="gray")

    def _setup_bindings(self):
        """Setup key bindings."""
        self.message_entry.bind('<Return>', lambda e: self._send_message())
        self.message_entry.focus()

    def _show_settings(self):
        """Show the settings dialog."""
        SettingsDialog(self)

    def _send_message(self):
        """Handle sending a message."""
        if self.is_processing:
            return

        message = self.message_var.get().strip()
        if not message:
            return

        if not self.config.get_api_key():
            messagebox.showerror(
                "Error",
                "Please configure your API key in Settings first."
            )
            return

        # Show loading state
        self.is_processing = True
        self.loading_label.grid()
        self.send_button.config(state=tk.DISABLED)
        self.message_entry.config(state=tk.DISABLED)

        # Enable chat history for editing
        self.chat_history.config(state=tk.NORMAL)
        
        # Add user message
        self.chat_history.insert(tk.END, f"You: {message}\n", "user")
        self.chat_history.see(tk.END)
        
        # Clear input field
        self.message_var.set("")

        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_message, args=(message,))
        thread.daemon = True
        thread.start()

    def _process_message(self, message):
        """Process the message in a separate thread."""
        try:
            # Initialize OpenAI service if needed
            if not self.openai_service:
                self.openai_service = OpenAIService(self.config.get_api_key())

            # Get response from OpenAI
            response = self.openai_service.send_message(message)

            # Update UI in the main thread
            self.after(0, self._update_chat_with_response, response)

        except OpenAIServiceError as e:
            # Show error in the chat
            self.after(0, self._show_error, str(e))
        except Exception as e:
            # Show unexpected error
            self.after(0, self._show_error, f"An unexpected error occurred: {str(e)}")
        finally:
            # Reset UI state in the main thread
            self.after(0, self._reset_ui_state)

    def _update_chat_with_response(self, response):
        """Update chat history with AI response."""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"Bot: {response}\n\n", "bot")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def _show_error(self, error_message):
        """Show error message in chat history."""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, f"Error: {error_message}\n\n", "error")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def _reset_ui_state(self):
        """Reset UI state after processing."""
        self.is_processing = False
        self.loading_label.grid_remove()
        self.send_button.config(state=tk.NORMAL)
        self.message_entry.config(state=tk.NORMAL)
        self.message_entry.focus()

    def run(self):
        """Start the application main loop."""
        self.mainloop()

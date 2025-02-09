"""Settings dialog for the chatbot application."""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

from ..utils.config import Config
from ..services.openai_service import OpenAIService, OpenAIServiceError

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config = Config()
        
        self.title("Settings")
        self.geometry("400x150")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_current_settings()
        
        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self):
        """Create and arrange widgets."""
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # API Key entry
        ttk.Label(main_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(main_frame, textvariable=self.api_key_var, width=40)
        self.api_key_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.E))
        
        ttk.Button(button_frame, text="Save", command=self._save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT)

    def _load_current_settings(self):
        """Load current settings into the form."""
        self.api_key_var.set(self.config.get_api_key())

    def _validate_api_key(self, api_key):
        """Validate the API key format."""
        # Basic validation for OpenAI API key format
        pattern = r'^sk-[A-Za-z0-9]{48}$'
        return bool(re.match(pattern, api_key))

    def _save_settings(self):
        """Save the settings."""
        api_key = self.api_key_var.get().strip()
        
        if not api_key:
            messagebox.showerror("Error", "API Key cannot be empty.")
            return
            
        if not self._validate_api_key(api_key):
            messagebox.showerror("Error", "Invalid API Key format. It should start with 'sk-' followed by 48 characters.")
            return

        # Try to initialize OpenAI service with new key
        try:
            test_service = OpenAIService(api_key)
            # If successful, save the key and update parent's service
            self.config.set_api_key(api_key)
            self.parent.openai_service = test_service
            messagebox.showinfo("Success", "API key validated and saved successfully!")
            self.destroy()
        except OpenAIServiceError as e:
            messagebox.showerror("Error", f"Failed to initialize OpenAI service: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

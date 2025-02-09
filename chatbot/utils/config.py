"""Configuration management for the chatbot application."""
import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / '.chatbot_config.json'

class Config:
    def __init__(self):
        self.config_data = self._load_config()

    def _load_config(self):
        """Load configuration from file or create default."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return self._get_default_config()
        return self._get_default_config()

    def _get_default_config(self):
        """Return default configuration."""
        return {
            'api_key': '',
            'theme': 'light'
        }

    def save_config(self):
        """Save current configuration to file."""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config_data, f, indent=4)

    def get_api_key(self):
        """Get OpenAI API key."""
        return self.config_data.get('api_key', '')

    def set_api_key(self, api_key):
        """Set OpenAI API key."""
        self.config_data['api_key'] = api_key
        self.save_config()
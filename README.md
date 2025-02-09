# ChatBot Application

A desktop chatbot application powered by OpenAI's GPT models. This application provides a user-friendly interface for interacting with AI, with support for conversation history and customizable settings.

## Features

- Clean and intuitive user interface
- Real-time chat interactions
- Conversation history
- Customizable settings
- Single executable distribution

## Installation

### Option 1: Using the Pre-built Executable (Windows)

1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `ChatBot.exe`

### Option 2: Building from Source

#### Prerequisites

- Python 3.8 or higher
- Git

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Code25356/game2.git
   cd game2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the executable:
   ```bash
   python build.py
   ```

   The executable will be created in the `dist` directory.

## Usage

1. Launch the application by running `ChatBot.exe`
2. Enter your OpenAI API key in the settings (first-time setup)
3. Start chatting with the AI in the main window
4. Use the settings menu to customize the application behavior

## Configuration

The application stores its configuration in a local settings file. You can configure:

- OpenAI API key
- Model selection
- UI preferences
- Chat history settings

## Development

### Project Structure

```
chatbot/
├── main.py           # Application entry point
├── services/         # Backend services
├── ui/              # User interface components
└── utils/           # Utility functions and configurations
```

### Building the Application

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

   This will:
   - Clean previous builds
   - Create a single-file executable
   - Package all dependencies
   - Configure Windows subsystem settings

### Testing

Before distributing:
1. Test the executable on a clean Windows system
2. Verify all features work correctly
3. Check that no Python installation is required
4. Test settings persistence
5. Verify chat functionality

## Troubleshooting

### Common Issues

1. **Executable won't start**
   - Verify Windows Defender isn't blocking the application
   - Check for missing Visual C++ Redistributable

2. **API Key Issues**
   - Ensure the API key is entered correctly
   - Check internet connectivity

3. **Performance Issues**
   - Clear chat history
   - Restart the application

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""OpenAI service integration."""
from typing import List, Dict, Optional
import openai
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, AuthenticationError

class OpenAIServiceError(Exception):
    """Base exception class for OpenAI service errors."""
    pass

class OpenAIService:
    def __init__(self, api_key: str):
        """Initialize the OpenAI service with the provided API key."""
        self.api_key = api_key
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise OpenAIServiceError(f"Failed to initialize OpenAI client: {str(e)}")
        
        self.conversation_history: List[Dict[str, str]] = []
        self.model = "gpt-3.5-turbo"

    def send_message(self, message: str) -> str:
        """
        Send a message to OpenAI API and get the response.
        
        Args:
            message: The user's message to send to the API
            
        Returns:
            str: The AI's response
            
        Raises:
            OpenAIServiceError: If there's any error in communicating with the API
        """
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Create the API request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and store the response
            ai_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            return ai_message

        except AuthenticationError as e:
            raise OpenAIServiceError("Invalid API key. Please check your OpenAI API key in settings.") from e
        except RateLimitError as e:
            raise OpenAIServiceError("Rate limit exceeded. Please try again later.") from e
        except APIConnectionError as e:
            raise OpenAIServiceError("Network error. Please check your internet connection.") from e
        except APIError as e:
            raise OpenAIServiceError(f"OpenAI API error: {str(e)}") from e
        except Exception as e:
            raise OpenAIServiceError(f"Unexpected error: {str(e)}") from e

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

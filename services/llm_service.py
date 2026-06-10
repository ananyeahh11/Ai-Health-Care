"""
LLM Service — handles all interactions with the Google Gemini API.
"""

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from utils.helper import load_prompt
from utils.constants import MODEL_NAME, MAX_OUTPUT_TOKENS, TEMPERATURE


class LLMService:
    """Service for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize the Gemini model with API key and prompts."""
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key or api_key == "your_api_key_here":
            raise ValueError(
                "Please set your GOOGLE_API_KEY in the .env file. "
                "Get a free key from https://aistudio.google.com/"
            )

        genai.configure(api_key=api_key)

        # Load prompts
        self.system_prompt = load_prompt("prompts/system_prompt.txt")
        self.safety_prompt = load_prompt("prompts/safety_prompt.txt")

        # Configure model
        self.generation_config = genai.types.GenerationConfig(
            max_output_tokens=MAX_OUTPUT_TOKENS,
            temperature=TEMPERATURE,
        )

        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=self.generation_config,
            system_instruction=self.system_prompt + "\n\n" + self.safety_prompt,
        )

    def generate_response(self, prompt: str, chat_history: list = None) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: The user's message or assembled prompt.
            chat_history: Optional list of previous messages for context.

        Returns:
            The model's response text.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if chat_history:
                    chat = self.model.start_chat(history=chat_history)
                    response = chat.send_message(prompt)
                else:
                    response = self.model.generate_content(prompt)

                return response.text

            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "rate" in error_str:
                    wait_time = (2 ** attempt) * 2
                    time.sleep(wait_time)
                    if attempt == max_retries - 1:
                        return (
                            "I'm currently experiencing high demand. "
                            "Please try again in a few moments. 🙏"
                        )
                elif "api_key" in error_str or "authentication" in error_str:
                    return (
                        "⚠️ API key error. Please check your GOOGLE_API_KEY "
                        "in the .env file."
                    )
                else:
                    if attempt == max_retries - 1:
                        return (
                            "I encountered an issue generating a response. "
                            "Please try again. If the problem persists, "
                            "check your internet connection."
                        )

        return "Unable to generate a response at this time. Please try again later."

    def generate_assessment_response(self, category: str, user_data: dict, context: str = "") -> str:
        """
        Generate an assessment analysis for a specific wellness category.

        Args:
            category: The wellness category (sleep, stress, diet, screen_time).
            user_data: Dictionary of user's questionnaire responses.
            context: Additional context from data files.

        Returns:
            AI-generated assessment analysis.
        """
        prompt = f"""
Analyze the following {category} assessment data for a student and provide:
1. A brief summary of their current {category} habits
2. A score estimation (out of 100) for their {category} wellness
3. 3-5 specific, actionable improvement tips
4. Whether they should consider consulting a professional

Student's {category.replace('_', ' ')} data:
{self._format_data(user_data)}

{f"Reference guidelines: {context}" if context else ""}

Remember: Provide general wellness awareness only. This is NOT medical advice.
"""
        return self.generate_response(prompt)

    def generate_routine(self, user_data: dict, routine_prompt: str) -> str:
        """
        Generate a personalized daily routine.

        Args:
            user_data: Dictionary of all user assessment data.
            routine_prompt: The routine generator prompt template.

        Returns:
            AI-generated daily routine.
        """
        prompt = f"""
{routine_prompt}

User's assessment data:
{self._format_data(user_data)}

Generate a personalized daily routine based on this data.
"""
        return self.generate_response(prompt)

    def _format_data(self, data: dict) -> str:
        """Format a dictionary into readable text for the prompt."""
        lines = []
        for key, value in data.items():
            clean_key = key.replace("_", " ").title()
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            lines.append(f"- {clean_key}: {value}")
        return "\n".join(lines)

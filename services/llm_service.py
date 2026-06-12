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
                
                print("GEMINI ERROR:", e)

                error_str = str(e).lower()

                if "429" in error_str or "rate" in error_str:
                    wait_time = (2 ** attempt) * 2
                    time.sleep(wait_time)

                    if attempt == max_retries - 1:
                        return """
## 🤖 AI Wellness Analysis

The AI analysis service is temporarily unavailable due to usage limits.

Your wellness score and assessment have been calculated successfully.

Please review the personalized recommendations and wellness tips provided below.

You may try again after a short wait for a more detailed AI-generated analysis.
"""

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

    def generate_assessment_response(
        self,
        category: str,
        user_data: dict,
        context: str = ""
    ) -> str:
        """
        Generate an assessment analysis for a specific wellness category.
        """

        prompt = f"""
You are a wellness assistant.

IMPORTANT:
The score below has already been calculated by the application.

Use that score when writing the analysis.

Score Interpretation:
0-39 = Needs Attention
40-69 = Fair
70-100 = Good

Student's {category.replace('_', ' ')} assessment:
Calculated Score: {user_data.get("calculated_score")}
Status: {user_data.get("status")}

{self._format_data(user_data)}

{f"Reference guidelines: {context}" if context else ""}

Provide:

1. Summary of habits
2. Explain why the score was received
3. Strengths
4. Weaknesses
5. 3-5 improvement tips

Rules:
- Use the provided calculated_score.
- Do NOT estimate another score.
- Do NOT contradict the provided score.
- Do NOT say the user is doing great if the score is low.
- If score < 40, clearly explain the areas needing attention.
- For score 40-69, give balanced feedback.
- If score >= 70, highlight positive habits.
- Avoid phrases like:
  "You're doing great"
  "Excellent overall"
  "Fantastic overall"
  when score < 40.

Remember:
This is general wellness awareness only, not medical advice.
"""

        return self.generate_response(prompt)

    def generate_routine(self, user_data: dict, routine_prompt: str) -> str:
        """
        Generate a personalized daily routine.
        """

        prompt = f"""
{routine_prompt}

User's assessment data:
{self._format_data(user_data)}

Generate a personalized daily routine based on this data.
"""

        return self.generate_response(prompt)

    def _format_data(self, data: dict) -> str:
        """
        Format a dictionary into readable text for the prompt.
        """

        lines = []

        for key, value in data.items():
            clean_key = key.replace("_", " ").title()

            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)

            lines.append(f"- {clean_key}: {value}")

        return "\n".join(lines)
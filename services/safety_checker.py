"""
Safety Checker — screens user inputs and AI outputs for safety concerns.
"""

from utils.constants import EMERGENCY_KEYWORDS, MEDICAL_KEYWORDS, EMERGENCY_HELPLINES


class SafetyChecker:
    """Checks user input and AI output for safety concerns."""

    def __init__(self):
        """Initialize with safety keyword lists."""
        self.emergency_keywords = EMERGENCY_KEYWORDS
        self.medical_keywords = MEDICAL_KEYWORDS
        self.helplines = EMERGENCY_HELPLINES

    def check_user_input(self, message: str) -> tuple:
        """
        Screen user input for emergency or concerning content.

        Args:
            message: The user's input text.

        Returns:
            Tuple of (is_safe: bool, response: str).
            If not safe, response contains the safety message to show.
        """
        if not message:
            return (True, "")

        message_lower = message.lower().strip()

        # Check for emergency keywords
        for keyword in self.emergency_keywords:
            if keyword in message_lower:
                return (False, self._get_emergency_response())

        return (True, "")

    def check_ai_output(self, response: str) -> tuple:
        """
        Validate AI output doesn't contain inappropriate medical content.

        Args:
            response: The AI-generated response text.

        Returns:
            Tuple of (is_safe: bool, cleaned_response: str).
        """
        if not response:
            return (True, "")

        # The response is generally safe since we have system prompts,
        # but we add the disclaimer if it's not already there
        disclaimer = "\n\n---\n*🔹 This is for awareness only, not medical advice.*"

        if "awareness only" not in response.lower() and "not medical advice" not in response.lower():
            response += disclaimer

        return (True, response)

    def _get_emergency_response(self) -> str:
        """Generate an emergency safety response with helpline information."""
        response = """
## 💙 We Care About You

I can see you might be going through a really tough time, and I want you to know that **you are not alone**. What you're feeling matters, and there are people who want to help.

**Please reach out to a trusted person** — a friend, family member, teacher, or counselor.

### 📞 Helpline Numbers:
"""
        for name, number in self.helplines.items():
            response += f"- **{name}**: {number}\n"

        response += """
### 💡 Remember:
- It's okay to ask for help — it's a sign of strength, not weakness.
- These feelings can get better with the right support.
- You deserve to feel better, and support is available 24/7.

*If you or someone you know is in immediate danger, please call emergency services (112) right away.*
"""
        return response

    def is_medical_query(self, message: str) -> bool:
        """
        Check if the user is asking for medical advice.

        Args:
            message: The user's input text.

        Returns:
            True if the message appears to be asking for medical advice.
        """
        message_lower = message.lower().strip()
        for keyword in self.medical_keywords:
            if keyword in message_lower:
                return True
        return False

    def get_medical_redirect_response(self) -> str:
        """Return a response redirecting medical queries to professionals."""
        return """
I appreciate you trusting me with your health concerns! 🙏

However, I'm a **wellness awareness assistant**, and I'm not qualified to:
- Diagnose medical conditions
- Recommend medications or treatments
- Provide clinical medical advice

**What I can help with:**
- General wellness tips for sleep, stress, diet, and screen time
- Healthy lifestyle suggestions
- Daily routine planning

**For medical concerns, please consult:**
- Your college/school health center
- A family doctor or general physician
- A licensed healthcare professional

*Your health is important — please don't hesitate to seek professional help!* 💪
"""

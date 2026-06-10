"""
Routine Generator — creates personalized daily routines for students.
"""

from utils.helper import load_json, load_prompt


class RoutineGenerator:
    """Generates personalized daily routines based on assessment data."""

    def __init__(self, llm_service):
        """
        Initialize with LLM service and load routine data.

        Args:
            llm_service: An instance of LLMService.
        """
        self.llm = llm_service
        self.routines_data = load_json("data/routines.json")
        self.routine_prompt = load_prompt("prompts/routine_generator_prompt.txt")

    def generate_routine(self, user_data: dict, preferences: dict = None) -> str:
        """
        Generate a personalized daily routine using the LLM.

        Args:
            user_data: Dictionary of all assessment results.
            preferences: Optional dict with user preferences (wake time, schedule type, etc.).

        Returns:
            AI-generated daily routine as formatted text.
        """
        # Build context from assessment data
        context = self._build_context(user_data, preferences)

        prompt = f"""
{self.routine_prompt}

{context}

Please generate a detailed, personalized daily routine for this student.
Format it as a clear time-based schedule.
"""
        return self.llm.generate_response(prompt)

    def get_template_routine(self, template_name: str) -> dict:
        """
        Get a pre-built routine template.

        Args:
            template_name: Name of the template (balanced_day, exam_period, relaxation_day).

        Returns:
            Dict with the template routine data.
        """
        templates = self.routines_data.get("templates", {})
        return templates.get(template_name, templates.get("balanced_day", {}))

    def get_morning_routine(self) -> list:
        """Get the suggested morning routine activities."""
        return self.routines_data.get("morning_routine", [])

    def get_evening_routine(self) -> list:
        """Get the suggested evening routine activities."""
        return self.routines_data.get("evening_routine", [])

    def get_study_breaks(self) -> list:
        """Get the suggested study break schedule."""
        return self.routines_data.get("study_breaks", [])

    def get_available_templates(self) -> list:
        """Get list of available routine template names."""
        templates = self.routines_data.get("templates", {})
        return [
            {"key": key, "name": val.get("name", key), "description": val.get("description", "")}
            for key, val in templates.items()
        ]

    def _build_context(self, user_data: dict, preferences: dict = None) -> str:
        """Build context string from user data for the LLM prompt."""
        context_parts = ["Student Assessment Summary:"]

        if user_data.get("sleep"):
            sleep = user_data["sleep"]
            context_parts.append(f"\nSleep (Score: {sleep.get('score', 'N/A')}/100):")
            context_parts.append(f"  - Status: {sleep.get('status', 'N/A')}")

        if user_data.get("stress"):
            stress = user_data["stress"]
            context_parts.append(f"\nStress (Score: {stress.get('score', 'N/A')}/100):")
            context_parts.append(f"  - Status: {stress.get('status', 'N/A')}")

        if user_data.get("diet"):
            diet = user_data["diet"]
            context_parts.append(f"\nDiet (Score: {diet.get('score', 'N/A')}/100):")
            context_parts.append(f"  - Status: {diet.get('status', 'N/A')}")

        if user_data.get("screen_time"):
            screen = user_data["screen_time"]
            context_parts.append(f"\nScreen Time (Score: {screen.get('score', 'N/A')}/100):")
            context_parts.append(f"  - Status: {screen.get('status', 'N/A')}")

        if preferences:
            context_parts.append(f"\nPreferences:")
            for key, value in preferences.items():
                context_parts.append(f"  - {key.replace('_', ' ').title()}: {value}")

        return "\n".join(context_parts)

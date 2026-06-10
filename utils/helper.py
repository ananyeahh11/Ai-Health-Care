"""
Utility / helper functions for the AI Health Awareness Agent.
"""

import json
import os
from datetime import datetime


def load_json(filepath: str) -> dict:
    """Load and return contents of a JSON file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_prompt(filepath: str) -> str:
    """Load and return contents of a prompt text file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def format_timestamp() -> str:
    """Return current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_report_filename(user_name: str) -> str:
    """Generate a unique report filename based on user name and timestamp."""
    safe_name = user_name.strip().replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"wellness_report_{safe_name}_{timestamp}.md"


def sanitize_text(text: str) -> str:
    """Remove potentially harmful content from text."""
    if not text:
        return ""
    return text.strip()


def calculate_score(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """
    Calculate a normalized score (0-100) from a value within a range.
    If invert=True, higher input values yield lower scores.
    """
    if max_val == min_val:
        return 50.0
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0.0, min(1.0, normalized))
    if invert:
        normalized = 1.0 - normalized
    return round(normalized * 100, 1)


def get_score_status(score: float) -> dict:
    """Return status info (label, color, emoji) for a given score."""
    if score >= 70:
        return {"label": "Good", "color": "#00BFA6", "emoji": "🟢"}
    elif score >= 40:
        return {"label": "Moderate", "color": "#FFB74D", "emoji": "🟡"}
    else:
        return {"label": "Needs Attention", "color": "#FF6584", "emoji": "🔴"}


def format_score_display(score: float) -> str:
    """Format score for display with status emoji."""
    status = get_score_status(score)
    return f"{status['emoji']} {score}/100 — {status['label']}"


def save_report(content: str, filename: str) -> str:
    """Save a report to the generated_reports directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(base_dir, "reports", "generated_reports")
    os.makedirs(reports_dir, exist_ok=True)
    filepath = os.path.join(reports_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def load_css(filepath: str) -> str:
    """Load CSS file and return as a string."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, filepath)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

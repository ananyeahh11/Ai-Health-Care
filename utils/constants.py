"""
Application-wide constants for AI Health Awareness Agent.
"""

# ──────────────────────────── App Metadata ────────────────────────────
APP_TITLE = "AI Health Awareness Agent"
APP_ICON = "🩺"
APP_DESCRIPTION = (
    "Your personal AI-powered wellness companion for students. "
    "Get safe, general health awareness tips around sleep, stress, diet, "
    "and study-life balance."
)

# ──────────────────────────── Disclaimer ──────────────────────────────
DISCLAIMER_TEXT = (
    "⚠️ **Disclaimer**: This tool is for awareness only, not medical advice. "
    "Always consult a qualified healthcare professional for medical concerns."
)

DISCLAIMER_SHORT = "This tool is for awareness only, not medical advice."

# ──────────────────────────── Categories ──────────────────────────────
CATEGORIES = {
    "sleep": {
        "name": "Sleep",
        "icon": "😴",
        "color": "#6C63FF",
        "description": "Assess your sleep patterns and get tips for better rest."
    },
    "stress": {
        "name": "Stress",
        "icon": "😰",
        "color": "#FF6584",
        "description": "Evaluate your stress levels and discover coping strategies."
    },
    "diet": {
        "name": "Diet",
        "icon": "🥗",
        "color": "#00BFA6",
        "description": "Review your eating habits and get nutrition awareness tips."
    },
    "screen_time": {
        "name": "Screen Time",
        "icon": "📱",
        "color": "#FFB74D",
        "description": "Analyze your digital habits and improve screen-life balance."
    }
}

# ──────────────────────────── Score Thresholds ────────────────────────
SCORE_THRESHOLDS = {
    "good": {"min": 70, "label": "Good", "color": "#00BFA6", "emoji": "🟢"},
    "moderate": {"min": 40, "label": "Moderate", "color": "#FFB74D", "emoji": "🟡"},
    "needs_attention": {"min": 0, "label": "Needs Attention", "color": "#FF6584", "emoji": "🔴"}
}

# ──────────────────────────── Emergency Helplines ─────────────────────
EMERGENCY_HELPLINES = {
    "Mental Health (India)": "iCall – 9152987821",
    "Suicide Prevention (India)": "AASRA – 9820466726",
    "Emergency (India)": "112",
    "Crisis Text Line": "Text HOME to 741741",
    "International Association for Suicide Prevention": "https://www.iasp.info/resources/Crisis_Centres/"
}

# ──────────────────────────── Model Config ────────────────────────────
MODEL_NAME = "gemini-2.5-flash"

MAX_OUTPUT_TOKENS = 2048
TEMPERATURE = 0.7

# ──────────────────────────── UI Colors ───────────────────────────────
COLORS = {
    "primary": "#6C63FF",
    "secondary": "#00BFA6",
    "accent": "#FF6584",
    "warning": "#FFB74D",
    "background_dark": "#0E1117",
    "background_card": "#1A1D23",
    "text_primary": "#FAFAFA",
    "text_secondary": "#B0B0B0",
    "border": "#2D2D2D"
}

# ──────────────────────────── Safety Keywords ─────────────────────────
EMERGENCY_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "self-harm", "self harm", "cutting myself", "hurt myself",
    "overdose", "not worth living", "no reason to live"
]

MEDICAL_KEYWORDS = [
    "prescribe", "prescription", "medication", "dosage", "medicine",
    "diagnose", "diagnosis", "treatment plan", "what disease",
    "what condition", "am i sick"
]

# ──────────────────────────── Assessment Defaults ─────────────────────
STRESS_SOURCES = [
    "Exams & Academics",
    "Assignments & Deadlines",
    "Social Pressure",
    "Financial Stress",
    "Family Issues",
    "Relationship Problems",
    "Health Concerns",
    "Future Uncertainty",
    "Other"
]

COPING_MECHANISMS = [
    "Exercise / Sports",
    "Talking to friends/family",
    "Meditation / Deep breathing",
    "Listening to music",
    "Watching shows / Gaming",
    "Journaling",
    "Sleeping",
    "Eating",
    "Nothing specific",
    "Other"
]

PHYSICAL_SYMPTOMS = [
    "Headaches",
    "Fatigue / Low energy",
    "Insomnia / Sleep problems",
    "Appetite changes",
    "Muscle tension",
    "Stomach issues",
    "Difficulty concentrating",
    "Rapid heartbeat",
    "None"
]

SCREEN_USE_TYPES = [
    "Studying / Online classes",
    "Social Media",
    "Gaming",
    "Entertainment (streaming)",
    "Work / Freelancing",
    "Communication (chat/calls)",
    "News / Browsing",
    "Other"
]

EXERCISE_FREQUENCY = [
    "Daily",
    "4-5 times a week",
    "2-3 times a week",
    "Once a week",
    "Rarely",
    "Never"
]

JUNK_FOOD_FREQUENCY = [
    "Daily",
    "A few times a week",
    "Once a week",
    "Rarely",
    "Never"
]

OVERWHELM_FREQUENCY = [
    "Almost every day",
    "A few times a week",
    "Once a week",
    "Rarely",
    "Never"
]

BREAK_FREQUENCY = [
    "Every 20 minutes",
    "Every 30 minutes",
    "Every hour",
    "Every 2 hours",
    "Rarely take breaks"
]

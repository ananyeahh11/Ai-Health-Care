"""
Score Calculator — pure math module for normalizing wellness scores.
"""

def calculate_sleep_score(answers: dict) -> float:
    """Calculate sleep wellness score (0-100)."""
    score = 50.0  # Base score

    hours = answers.get("hours", 7)
    if 7 <= hours <= 9:
        score += 20
    elif 6 <= hours < 7 or 9 < hours <= 10:
        score += 10
    elif hours < 5:
        score -= 15

    quality = answers.get("quality", 5)
    score += (quality - 5) * 5

    env_quality = answers.get("environment_quality", 5)
    score += (env_quality - 5) * 3

    if not answers.get("caffeine_after_2pm", False):
        score += 5

    if not answers.get("naps", False) or hours >= 7:
        score += 5

    return max(0, min(100, round(score, 1)))


def calculate_stress_score(answers: dict) -> float:
    """Calculate stress wellness score (0-100). Higher = less stressed."""
    level = answers.get("level", 5)
    score = 100 - (level * 10)  # Invert: low stress = high score

    symptoms = answers.get("physical_symptoms", [])
    symptom_count = len([s for s in symptoms if s != "None"])
    score -= symptom_count * 3

    overwhelm = answers.get("overwhelm_frequency", "Rarely")
    overwhelm_penalty = {
        "Almost every day": -15,
        "A few times a week": -10,
        "Once a week": -5,
        "Rarely": 0,
        "Never": 5
    }
    score += overwhelm_penalty.get(overwhelm, 0)

    coping = answers.get("coping_mechanisms", [])
    positive_coping = ["Exercise / Sports", "Talking to friends/family",
                      "Meditation / Deep breathing", "Journaling"]
    positive_count = len([c for c in coping if c in positive_coping])
    score += positive_count * 3

    exercise = answers.get("exercise_frequency", "Rarely")
    exercise_bonus = {
        "Daily": 10, "4-5 times a week": 8, "2-3 times a week": 5,
        "Once a week": 2, "Rarely": -3, "Never": -5
    }
    score += exercise_bonus.get(exercise, 0)

    return max(0, min(100, round(score, 1)))


def calculate_diet_score(answers: dict) -> float:
    """Calculate diet wellness score (0-100)."""
    score = 50.0

    meals = answers.get("meals_per_day", 3)
    if meals == 3:
        score += 15
    elif meals == 2:
        score += 5
    elif meals < 2:
        score -= 10

    if not answers.get("skips_breakfast", True):
        score += 10
    else:
        score -= 10

    water = answers.get("water_glasses", 4)
    if water >= 8:
        score += 15
    elif water >= 5:
        score += 8
    elif water < 3:
        score -= 10

    fruit_veg = answers.get("fruit_veg_servings", 2)
    if fruit_veg >= 5:
        score += 15
    elif fruit_veg >= 3:
        score += 8
    elif fruit_veg < 2:
        score -= 5

    junk = answers.get("junk_food_frequency", "A few times a week")
    junk_penalty = {
        "Daily": -15, "A few times a week": -8, "Once a week": 0,
        "Rarely": 5, "Never": 10
    }
    score += junk_penalty.get(junk, 0)

    if not answers.get("late_night_eating", False):
        score += 5

    return max(0, min(100, round(score, 1)))


def calculate_screen_time_score(answers: dict) -> float:
    """Calculate screen time wellness score (0-100)."""
    score = 50.0

    daily = answers.get("daily_hours", 6)
    if daily <= 4:
        score += 20
    elif daily <= 6:
        score += 10
    elif daily <= 8:
        score += 0
    elif daily <= 10:
        score -= 10
    else:
        score -= 20

    if answers.get("takes_breaks", True):
        score += 10

        freq = answers.get("break_frequency", "Every hour")
        freq_bonus = {
            "Every 20 minutes": 10, "Every 30 minutes": 7,
            "Every hour": 3, "Every 2 hours": 0, "Rarely take breaks": -5
        }
        score += freq_bonus.get(freq, 0)

    if not answers.get("screen_before_bed", True):
        score += 10

    if not answers.get("eye_strain", False):
        score += 5

    social = answers.get("social_media_hours", 2)
    if social <= 1:
        score += 10
    elif social <= 2:
        score += 5
    elif social > 4:
        score -= 10

    return max(0, min(100, round(score, 1)))

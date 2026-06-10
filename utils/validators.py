"""
Input validators for assessment questionnaires.
"""


def validate_sleep_input(data: dict) -> tuple:
    """
    Validate sleep assessment inputs.
    Returns (is_valid: bool, errors: list[str]).
    """
    errors = []

    hours = data.get("hours", 0)
    if not (0 <= hours <= 24):
        errors.append("Sleep hours must be between 0 and 24.")

    quality = data.get("quality", 0)
    if not (1 <= quality <= 10):
        errors.append("Sleep quality must be between 1 and 10.")

    environment = data.get("environment_quality", 0)
    if not (1 <= environment <= 10):
        errors.append("Environment quality must be between 1 and 10.")

    return (len(errors) == 0, errors)


def validate_stress_input(data: dict) -> tuple:
    """
    Validate stress assessment inputs.
    Returns (is_valid: bool, errors: list[str]).
    """
    errors = []

    level = data.get("level", 0)
    if not (1 <= level <= 10):
        errors.append("Stress level must be between 1 and 10.")

    stressors = data.get("stressors", [])
    if not stressors:
        errors.append("Please select at least one stressor.")

    return (len(errors) == 0, errors)


def validate_diet_input(data: dict) -> tuple:
    """
    Validate diet assessment inputs.
    Returns (is_valid: bool, errors: list[str]).
    """
    errors = []

    meals = data.get("meals_per_day", 0)
    if not (1 <= meals <= 8):
        errors.append("Meals per day must be between 1 and 8.")

    water = data.get("water_glasses", 0)
    if not (0 <= water <= 20):
        errors.append("Water intake must be between 0 and 20 glasses.")

    fruit_veg = data.get("fruit_veg_servings", 0)
    if not (0 <= fruit_veg <= 15):
        errors.append("Fruit/vegetable servings must be between 0 and 15.")

    return (len(errors) == 0, errors)


def validate_screen_time_input(data: dict) -> tuple:
    """
    Validate screen time assessment inputs.
    Returns (is_valid: bool, errors: list[str]).
    """
    errors = []

    daily_hours = data.get("daily_hours", 0)
    if not (0 <= daily_hours <= 24):
        errors.append("Daily screen hours must be between 0 and 24.")

    social_hours = data.get("social_media_hours", 0)
    if not (0 <= social_hours <= 24):
        errors.append("Social media hours must be between 0 and 24.")

    if social_hours > daily_hours:
        errors.append("Social media hours cannot exceed total screen time.")

    primary_use = data.get("primary_use", [])
    if not primary_use:
        errors.append("Please select at least one primary screen use.")

    return (len(errors) == 0, errors)


def validate_age(age: int) -> bool:
    """Validate user age is within a reasonable range."""
    return 10 <= age <= 100


def validate_name(name: str) -> bool:
    """Validate user name is not empty and has reasonable length."""
    return bool(name) and 1 <= len(name.strip()) <= 100

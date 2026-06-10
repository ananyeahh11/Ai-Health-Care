"""
Pydantic models for user profile and assessment data.
"""

from pydantic import BaseModel, Field
from typing import Optional


class SleepAssessment(BaseModel):
    """Data model for sleep assessment questionnaire responses."""
    bedtime: str = Field(description="Usual bedtime (e.g., '11:00 PM')")
    wake_time: str = Field(description="Usual wake-up time (e.g., '7:00 AM')")
    quality: int = Field(ge=1, le=10, description="Sleep quality rating 1-10")
    hours: float = Field(ge=0, le=24, description="Hours of sleep per night")
    naps: bool = Field(description="Whether user takes naps")
    caffeine_after_2pm: bool = Field(description="Caffeine consumption after 2 PM")
    environment_quality: int = Field(ge=1, le=10, description="Sleep environment quality 1-10")


class StressAssessment(BaseModel):
    """Data model for stress assessment questionnaire responses."""
    level: int = Field(ge=1, le=10, description="Current stress level 1-10")
    stressors: list = Field(description="List of main stress sources")
    overwhelm_frequency: str = Field(description="How often feeling overwhelmed")
    coping_mechanisms: list = Field(description="Current coping strategies")
    physical_symptoms: list = Field(description="Stress-related physical symptoms")
    exercise_frequency: str = Field(description="How often user exercises")


class DietAssessment(BaseModel):
    """Data model for diet assessment questionnaire responses."""
    meals_per_day: int = Field(ge=1, le=8, description="Number of meals per day")
    skips_breakfast: bool = Field(description="Whether user skips breakfast")
    water_glasses: int = Field(ge=0, le=20, description="Glasses of water per day")
    fruit_veg_servings: int = Field(ge=0, le=15, description="Fruit/vegetable servings per day")
    junk_food_frequency: str = Field(description="How often user eats junk food")
    late_night_eating: bool = Field(description="Whether user eats late at night")
    dietary_restrictions: str = Field(default="", description="Any dietary restrictions")


class ScreenTimeAssessment(BaseModel):
    """Data model for screen time assessment questionnaire responses."""
    daily_hours: float = Field(ge=0, le=24, description="Total daily screen hours")
    primary_use: list = Field(description="Primary reasons for screen use")
    takes_breaks: bool = Field(description="Whether user takes regular breaks")
    break_frequency: str = Field(description="How often breaks are taken")
    screen_before_bed: bool = Field(description="Screen use before bedtime")
    eye_strain: bool = Field(description="Whether user experiences eye strain")
    social_media_hours: float = Field(ge=0, le=24, description="Daily social media hours")


class UserProfile(BaseModel):
    """Complete user profile with all assessment data."""
    name: str = Field(description="User's name")
    age: int = Field(ge=10, le=100, description="User's age")
    student_type: str = Field(description="Type: school, college, or postgrad")
    sleep_data: Optional[SleepAssessment] = None
    stress_data: Optional[StressAssessment] = None
    diet_data: Optional[DietAssessment] = None
    screen_time_data: Optional[ScreenTimeAssessment] = None

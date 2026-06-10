"""
Pydantic models for wellness reports.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryScore(BaseModel):
    """Score and analysis for a single wellness category."""
    category: str = Field(description="Category name: sleep, stress, diet, or screen_time")
    score: float = Field(ge=0, le=100, description="Score from 0-100")
    status: str = Field(description="Status: good, moderate, or needs_attention")
    key_findings: list = Field(default_factory=list, description="Key observations")
    recommendations: list = Field(default_factory=list, description="Personalized recommendations")


class WellnessReport(BaseModel):
    """Complete wellness report aggregating all assessments."""
    user_name: str = Field(description="User's name")
    user_age: int = Field(description="User's age")
    student_type: str = Field(description="Type of student")
    overall_score: float = Field(ge=0, le=100, description="Overall wellness score 0-100")
    category_scores: list = Field(default_factory=list, description="List of CategoryScore objects")
    daily_routine: Optional[str] = Field(default=None, description="Generated daily routine")
    generated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    disclaimer: str = Field(
        default="This report is for awareness only, not medical advice. "
                "Always consult a qualified healthcare professional for medical concerns."
    )

    def to_markdown(self) -> str:
        """Convert the report to a markdown string for download."""
        md = f"# 🩺 Wellness Report for {self.user_name}\n\n"
        md += f"**Generated:** {self.generated_at}\n\n"
        md += f"**Age:** {self.user_age} | **Student Type:** {self.student_type}\n\n"
        md += f"---\n\n"
        md += f"## Overall Wellness Score: {self.overall_score}/100\n\n"

        for cat_score in self.category_scores:
            if isinstance(cat_score, dict):
                cat = cat_score
            else:
                cat = cat_score.dict() if hasattr(cat_score, 'dict') else cat_score

            category_name = cat.get('category', 'Unknown').replace('_', ' ').title()
            score = cat.get('score', 0)
            status = cat.get('status', 'unknown')

            status_emoji = "🟢" if status == "good" else "🟡" if status == "moderate" else "🔴"

            md += f"### {status_emoji} {category_name}: {score}/100 ({status.replace('_', ' ').title()})\n\n"

            findings = cat.get('key_findings', [])
            if findings:
                md += "**Key Findings:**\n"
                for finding in findings:
                    md += f"- {finding}\n"
                md += "\n"

            recommendations = cat.get('recommendations', [])
            if recommendations:
                md += "**Recommendations:**\n"
                for rec in recommendations:
                    md += f"- {rec}\n"
                md += "\n"

            md += "---\n\n"

        if self.daily_routine:
            md += f"## 📋 Suggested Daily Routine\n\n{self.daily_routine}\n\n---\n\n"

        md += f"> ⚠️ **Disclaimer:** {self.disclaimer}\n"
        return md
